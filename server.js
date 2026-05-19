require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { OAuth2Client } = require('google-auth-library');
const axios = require('axios');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret_change_in_env';

// ✅ SAFE FALLBACKS FOR ADMIN CREDENTIALS
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@laptoptracker.com';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin232';

app.use(helmet({
  contentSecurityPolicy: false,
  crossOriginEmbedderPolicy: false
}));
app.use(cors({ origin: ['https://laptop-tracker-2h7l.onrender.com', 'http://localhost:3000'], credentials: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// RATE LIMITING
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: { error: 'Too many attempts. Please try again in 15 minutes.' },
  standardHeaders: true,
  legacyHeaders: false,
});
const apiLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 60,
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/auth/', authLimiter);
app.use('/api/', apiLimiter);

// GOOGLE CONFIG
const GOOGLE_CLIENT_ID = "725032797775-iam91nooik7abniqg41hjejso90f2asr.apps.googleusercontent.com";
const googleClient = new OAuth2Client(GOOGLE_CLIENT_ID);

// M-PESA CONFIG
const MPESA_CONSUMER_KEY = process.env.MPESA_CONSUMER_KEY;
const MPESA_CONSUMER_SECRET = process.env.MPESA_CONSUMER_SECRET;
const MPESA_SHORTCODE = process.env.MPESA_SHORTCODE;
const MPESA_PASSKEY = process.env.MPESA_PASSKEY;
const MPESA_CALLBACK_URL = process.env.MPESA_CALLBACK_URL;
const MPESA_BASE_URL = process.env.MPESA_BASE_URL;
const pendingPayments = new Map();

// JSON DATABASE
const DB_FILE = './data.json';
const loadDB = () => {
  try { return JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); }
  catch { return { users: [], laptops: [] }; }
};
const saveDB = (data) => fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
if (!fs.existsSync(DB_FILE)) saveDB({ users: [], laptops: [] });

// ADMIN HELPER
const isAdmin = (user) => user && user.email === ADMIN_EMAIL;

// ✅ AUTO-CREATE / FIX ADMIN ON STARTUP
(async () => {
  const db = loadDB();
  const adminUser = db.users.find(u => u.email === ADMIN_EMAIL);
  
  if (!adminUser) {
    const hashed = await bcrypt.hash(ADMIN_PASSWORD, 10);
    db.users.push({
      id: 'admin_001',
      name: 'System Admin',
      email: ADMIN_EMAIL,
      password: hashed,
      role: 'admin',
      phone: '',
      trialEndDate: new Date().toISOString(),
      isSubscribed: true,
      subscriptionExpiryDate: new Date('2099-12-31').toISOString(),
      provider: 'local'
    });
    console.log('🔑 Admin account created securely.');
  } else {
    adminUser.role = 'admin';
    adminUser.isSubscribed = true;
    adminUser.subscriptionExpiryDate = new Date('2099-12-31').toISOString();
    console.log('✅ Admin account verified and unlocked.');
  }
  saveDB(db);
})();

const getSubscriptionStatus = (user) => {
  const now = new Date();
  const trialEnd = new Date(user.trialEndDate || Date.now());
  const subExpiry = user.subscriptionExpiryDate ? new Date(user.subscriptionExpiryDate) : null;
  if (now < trialEnd) return { status: 'trial', daysLeft: Math.ceil((trialEnd - now) / (1000 * 60 * 60 * 24)) };
  if (user.isSubscribed && subExpiry && now < subExpiry) return { status: 'active', expires: subExpiry.toISOString() };
  return { status: 'expired' };
};

const findOrCreateUser = (email, name, isGoogle) => {
  const db = loadDB();
  let user = db.users.find(u => u.email === email);
  if (!user) {
    const trialEndDate = new Date();
    trialEndDate.setDate(trialEndDate.getDate() + 21);
    user = {
      id: Date.now().toString(), name, email,
      password: isGoogle ? 'GOOGLE_USER_NO_PASSWORD' : 'N/A',
      role: 'user', phone: '',
      trialEndDate: trialEndDate.toISOString(),
      isSubscribed: false, subscriptionExpiryDate: null, provider: isGoogle ? 'google' : 'local'
    };
    db.users.push(user);
    saveDB(db);
  }
  return user;
};

// AUTH ROUTES
app.post('/api/auth/register', async (req, res) => {
  const { name, email, password } = req.body;
  const db = loadDB();
  if (db.users.find(u => u.email === email)) return res.status(400).json({ error: 'Email exists' });
  const hashed = await bcrypt.hash(password, 10);
  const trialEndDate = new Date();
  trialEndDate.setDate(trialEndDate.getDate() + 21);
  const user = {
    id: Date.now().toString(), name, email, password: hashed, role: 'user', phone: '',
    trialEndDate: trialEndDate.toISOString(), isSubscribed: false, subscriptionExpiryDate: null, provider: 'local'
  };
  db.users.push(user); saveDB(db);
  const token = jwt.sign({ id: user.id, role: user.role, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
  res.status(201).json({ token, user: { id: user.id, name, email, role: user.role } });
});

app.post('/api/auth/google', async (req, res) => {
  const { credential } = req.body;
  if (!credential) return res.status(400).json({ error: 'No credential' });
  try {
    const ticket = await googleClient.verifyIdToken({ idToken: credential, audience: GOOGLE_CLIENT_ID });
    const payload = ticket.getPayload();
    const user = findOrCreateUser(payload.email, payload.name, true);
    const token = jwt.sign({ id: user.id, role: user.role, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user.id, name: user.name, email: user.email, role: user.role } });
  } catch { res.status(401).json({ error: 'Invalid Google Token' }); }
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const db = loadDB();
  const user = db.users.find(u => u.email === email);
  if (!user) return res.status(400).json({ error: 'Invalid credentials' });
  const valid = await bcrypt.compare(password, user.password);
  if (!valid) return res.status(400).json({ error: 'Invalid credentials' });
  const token = jwt.sign({ id: user.id, role: user.role, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
  res.json({ token, user: { id: user.id, name: user.name, email, role: user.role } });
});

const protect = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Not authorized' });
  try { req.user = jwt.verify(token, JWT_SECRET); next(); }
  catch { res.status(401).json({ error: 'Invalid or expired token' }); }
};

// M-PESA
async function getMpesaAccessToken() {
  const auth = Buffer.from(`${MPESA_CONSUMER_KEY}:${MPESA_CONSUMER_SECRET}`).toString('base64');
  const res = await axios.get(`${MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials`, {
    headers: { Authorization: `Basic ${auth}` }
  });
  return res.data.access_token;
}
function generateMpesaPassword(timestamp) {
  return Buffer.from(MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).toString('base64');
}

app.post('/api/mpesa/pay', protect, async (req, res) => {
  try {
    const { phone, amount = 2500 } = req.body;
    if (!phone) return res.status(400).json({ error: 'Phone number required' });
    const formattedPhone = phone.replace(/\s/g, '').startsWith('254') ? phone.replace(/\s/g, '') : `254${phone.replace(/^0/, '')}`;
    const token = await getMpesaAccessToken();
    const timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);
    const payload = {
      BusinessShortCode: MPESA_SHORTCODE, Password: generateMpesaPassword(timestamp), Timestamp: timestamp,
      TransactionType: "CustomerPayBillOnline", Amount: amount, PartyA: formattedPhone, PartyB: MPESA_SHORTCODE,
      PhoneNumber: formattedPhone, CallBackURL: MPESA_CALLBACK_URL, AccountReference: "LaptopTracker", TransactionDesc: "Subscription"
    };
    const stkRes = await axios.post(`${MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    });
    pendingPayments.set(formattedPhone, { userId: req.user.id, amount, timestamp });
    res.json({ message: 'STK Push sent successfully. Check your phone.', CheckoutRequestID: stkRes.data.CheckoutRequestID });
  } catch (err) {
    console.error('M-Pesa Error:', err.response?.data || err.message);
    res.status(500).json({ error: 'Failed to initiate payment' });
  }
});

app.post('/api/mpesa/callback', async (req, res) => {
  try {
    const { Body } = req.body;
    const { stkCallback } = Body;
    res.json({ ResultCode: 0, ResultDesc: 'Success' });
    if (stkCallback.ResultCode === 0 && stkCallback.CallbackMetadata) {
      const phone = stkCallback.PhoneNumber || Object.values(stkCallback)[0]?.PhoneNumber;
      const pending = pendingPayments.get(phone);
      if (pending) {
        const db = loadDB();
        const idx = db.users.findIndex(u => u.id === pending.userId);
        if (idx !== -1) {
          const expiry = new Date(); expiry.setMonth(expiry.getMonth() + 4);
          db.users[idx].isSubscribed = true;
          db.users[idx].subscriptionExpiryDate = expiry.toISOString();
          db.users[idx].paymentHistory = db.users[idx].paymentHistory || [];
          db.users[idx].paymentHistory.push({ amount: pending.amount, currency: 'KSH', date: new Date().toISOString(), method: 'M-Pesa' });
          saveDB(db);
          pendingPayments.delete(phone);
        }
      }
    }
  } catch (err) { console.error('Callback Error:', err); res.status(500).json({ ResultCode: 1 }); }
});

app.get('/api/subscription/status', protect, (req, res) => {
  const db = loadDB();
  const user = db.users.find(u => u.id === req.user.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(getSubscriptionStatus(user));
});

app.post('/api/subscription/activate', protect, (req, res) => {
  const db = loadDB();
  const idx = db.users.findIndex(u => u.id === req.user.id);
  if (idx === -1) return res.status(404).json({ error: 'User not found' });
  const expiry = new Date(); expiry.setMonth(expiry.getMonth() + 4);
  db.users[idx].isSubscribed = true;
  db.users[idx].subscriptionExpiryDate = expiry.toISOString();
  db.users[idx].paymentHistory = db.users[idx].paymentHistory || [];
  db.users[idx].paymentHistory.push({ amount: 2500, currency: 'KSH', date: new Date().toISOString(), method: req.body.method || 'test' });
  saveDB(db);
  res.json({ message: 'Subscription activated', expires: expiry.toISOString() });
});

// ✅ ADMIN EXEMPT FROM SUBSCRIPTION CHECK
const checkSub = (req, res, next) => {
  const db = loadDB();
  const user = db.users.find(u => u.id === req.user.id);
  if (user && user.role === 'admin') return next();
  if (getSubscriptionStatus(user).status === 'expired') return res.status(403).json({ error: 'Subscription expired.' });
  next();
};

app.post('/api/laptops', protect, checkSub, (req, res) => {
  const db = loadDB();
  const laptop = { id: Date.now().toString(), user: req.user.id, ...req.body, status: req.body.status || 'Active', stolen: false, lastIpAddress: null, lastLocation: null, lastSeen: null };
  db.laptops.push(laptop); saveDB(db);
  res.status(201).json(laptop);
});
app.get('/api/laptops', protect, (req, res) => {
  const db = loadDB(); res.json(db.laptops.filter(l => l.user === req.user.id));
});
app.delete('/api/laptops/:id', protect, (req, res) => {
  const db = loadDB();
  db.laptops = db.laptops.filter(l => !(l.id === req.params.id && l.user === req.user.id));
  saveDB(db); res.json({ message: 'Deleted' });
});
app.put('/api/laptops/:id', protect, checkSub, (req, res) => {
  const db = loadDB();
  const idx = db.laptops.findIndex(l => l.id === req.params.id && l.user === req.user.id);
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  db.laptops[idx] = { ...db.laptops[idx], ...req.body };
  saveDB(db); res.json(db.laptops[idx]);
});
app.get('/api/laptops/:id/checkin', async (req, res) => {
  try {
    const db = loadDB();
    const laptop = db.laptops.find(l => l.id === req.params.id);
    if (!laptop) return res.status(404).json({ error: 'Not found' });
    const ip = req.headers['x-forwarded-for']?.split(',')[0] || req.connection.remoteAddress;
    try {
      const loc = await fetch(`http://ip-api.com/json/${ip}`).then(r => r.json());
      if (loc.status === 'success') {
        const idx = db.laptops.findIndex(l => l.id === req.params.id);
        db.laptops[idx].lastIpAddress = ip;
        db.laptops[idx].lastLocation = { city: loc.city, region: loc.regionName, country: loc.country, latitude: loc.lat, longitude: loc.lon, timezone: loc.timezone };
        db.laptops[idx].lastSeen = new Date().toISOString();
        saveDB(db);
      }
    } catch {}
    res.json({ message: 'Check-in successful' });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.put('/api/laptops/:id/stolen', protect, (req, res) => {
  const db = loadDB();
  const idx = db.laptops.findIndex(l => l.id === req.params.id);
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  if (db.laptops[idx].user !== req.user.id && !isAdmin(req.user)) return res.status(403).json({ error: 'Not authorized' });
  db.laptops[idx].stolen = req.body.stolen || true;
  db.laptops[idx].status = req.body.stolen ? 'Stolen' : 'Active';
  saveDB(db); res.json(db.laptops[idx]);
});
app.get('/api/laptops/:id/location', protect, (req, res) => {
  const db = loadDB();
  const laptop = db.laptops.find(l => l.id === req.params.id);
  if (!laptop) return res.status(404).json({ error: 'Not found' });
  if (laptop.user !== req.user.id && !isAdmin(req.user)) return res.status(403).json({ error: 'Not authorized' });
  res.json({ lastLocation: laptop.lastLocation, lastSeen: laptop.lastSeen, lastIpAddress: laptop.lastIpAddress, stolen: laptop.stolen });
});

// ADMIN ROUTES
app.get('/api/admin/users', protect, (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin access required' });
  const db = loadDB();
  res.json(db.users.map(u => ({ id: u.id, name: u.name, email: u.email, role: u.role, subscription: getSubscriptionStatus(u) })));
});
app.get('/api/admin/laptops', protect, (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin access required' });
  const db = loadDB();
  res.json(db.laptops.map(l => ({ ...l, ownerName: db.users.find(u => u.id === l.user)?.name || 'Unknown' })));
});
app.delete('/api/admin/laptops/:id', protect, (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin access required' });
  const db = loadDB();
  db.laptops = db.laptops.filter(l => l.id !== req.params.id);
  saveDB(db); res.json({ message: 'Deleted' });
});
app.get('/api/admin/stolen', protect, (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin access required' });
  const db = loadDB();
  res.json(db.laptops.filter(l => l.stolen).map(l => ({ ...l, ownerName: db.users.find(u => u.id === l.user)?.name || 'Unknown' })));
});

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.get('/dashboard', (req, res) => res.sendFile(path.join(__dirname, 'public', 'dashboard.html')));
app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'admin.html')));
app.get('/subscription', (req, res) => res.sendFile(path.join(__dirname, 'public', 'subscription.html')));
app.get('/checkin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'checkin.html')));

app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));