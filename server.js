require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { OAuth2Client } = require('google-auth-library');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// GOOGLE CONFIG
const GOOGLE_CLIENT_ID = "725032797775-iam91nooik7abniqg41hjejso90f2asr.apps.googleusercontent.com";
const googleClient = new OAuth2Client(GOOGLE_CLIENT_ID);

// JSON DATABASE
const DB_FILE = './data.json';
const loadDB = () => {
  try { return JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); }
  catch { return { users: [], laptops: [] }; }
};
const saveDB = (data) => fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
if (!fs.existsSync(DB_FILE)) saveDB({ users: [], laptops: [] });

const isAdmin = (user) => user && user.email === 'admin@laptoptracker.com';

// SUBSCRIPTION HELPER
const getSubscriptionStatus = (user) => {
  const now = new Date();
  const trialEnd = new Date(user.trialEndDate || Date.now());
  const subExpiry = user.subscriptionExpiryDate ? new Date(user.subscriptionExpiryDate) : null;
  if (now < trialEnd) return { status: 'trial', daysLeft: Math.ceil((trialEnd - now) / (1000 * 60 * 60 * 24)) };
  if (user.isSubscribed && subExpiry && now < subExpiry) return { status: 'active', expires: subExpiry.toISOString() };
  return { status: 'expired' };
};

// HELPER: Find or Create User
const findOrCreateUser = (email, name, isGoogle) => {
  const db = loadDB();
  let user = db.users.find(u => u.email === email);
  if (!user) {
    const trialEndDate = new Date();
    trialEndDate.setDate(trialEndDate.getDate() + 21);
    user = {
      id: Date.now().toString(), name, email, 
      password: isGoogle ? 'GOOGLE_USER_NO_PASSWORD' : 'N/A',
      role: 'user',
      trialEndDate: trialEndDate.toISOString(),
      isSubscribed: false, subscriptionExpiryDate: null,
      provider: isGoogle ? 'google' : 'local'
    };
    db.users.push(user);
    saveDB(db);
  }
  return user;
};

// REGISTER
app.post('/api/auth/register', (req, res) => {
  const { name, email, password } = req.body;
  const db = loadDB();
  if (db.users.find(u => u.email === email)) return res.status(400).json({ error: 'Email exists' });
  const trialEndDate = new Date();
  trialEndDate.setDate(trialEndDate.getDate() + 21);
  const user = {
    id: Date.now().toString(), name, email, password, role: 'user',
    trialEndDate: trialEndDate.toISOString(),
    isSubscribed: false, subscriptionExpiryDate: null, provider: 'local'
  };
  db.users.push(user);
  saveDB(db);
  const token = Buffer.from(JSON.stringify({ id: user.id, role: user.role })).toString('base64');
  res.status(201).json({ token, user: { id: user.id, name, email, role: user.role } });
});

// GOOGLE LOGIN
app.post('/api/auth/google', async (req, res) => {
  const { credential } = req.body;
  if (!credential) return res.status(400).json({ error: 'No credential' });
  try {
    const ticket = await googleClient.verifyIdToken({ idToken: credential, audience: GOOGLE_CLIENT_ID });
    const payload = ticket.getPayload();
    const user = findOrCreateUser(payload.email, payload.name, true);
    const token = Buffer.from(JSON.stringify({ id: user.id, role: user.role })).toString('base64');
    res.json({ token, user: { id: user.id, name: user.name, email: user.email, role: user.role } });
  } catch (error) {
    res.status(401).json({ error: 'Invalid Google Token' });
  }
});

// LOGIN
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  const db = loadDB();
  const user = db.users.find(u => u.email === email && u.password === password);
  if (!user) return res.status(400).json({ error: 'Invalid credentials' });
  const token = Buffer.from(JSON.stringify({ id: user.id, role: user.role })).toString('base64');
  res.json({ token, user: { id: user.id, name: user.name, email, role: user.role } });
});

const protect = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Not authorized' });
  try { req.user = JSON.parse(Buffer.from(token, 'base64').toString()); next(); }
  catch { res.status(401).json({ error: 'Invalid token' }); }
};

// SUBSCRIPTION API
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
  const now = new Date();
  const expiry = new Date();
  expiry.setMonth(expiry.getMonth() + 4);
  db.users[idx].isSubscribed = true;
  db.users[idx].subscriptionExpiryDate = expiry.toISOString();
  db.users[idx].paymentHistory = db.users[idx].paymentHistory || [];
  db.users[idx].paymentHistory.push({ amount: 2500, currency: 'KSH', date: now.toISOString(), method: req.body.method || 'test' });
  saveDB(db);
  res.json({ message: 'Subscription activated for 4 months', expires: expiry.toISOString() });
});

// LAPTOP ROUTES
const checkSub = (req, res, next) => {
  const db = loadDB();
  const user = db.users.find(u => u.id === req.user.id);
  if (getSubscriptionStatus(user).status === 'expired') {
    return res.status(403).json({ error: 'Subscription expired. Please renew.' });
  }
  next();
};

app.post('/api/laptops', protect, checkSub, (req, res) => {
  const db = loadDB();
  const laptop = { 
    id: Date.now().toString(), 
    user: req.user.id, 
    ...req.body, 
    status: req.body.status || 'Active', 
    stolen: false,
    lastIpAddress: null,
    lastLocation: null,
    lastSeen: null
  };
  db.laptops.push(laptop); 
  saveDB(db);
  res.status(201).json(laptop);
});

app.get('/api/laptops', protect, (req, res) => {
  const db = loadDB();
  res.json(db.laptops.filter(l => l.user === req.user.id));
});

app.delete('/api/laptops/:id', protect, (req, res) => {
  const db = loadDB();
  db.laptops = db.laptops.filter(l => !(l.id === req.params.id && l.user === req.user.id));
  saveDB(db); 
  res.json({ message: 'Deleted' });
});

app.put('/api/laptops/:id', protect, checkSub, (req, res) => {
  const db = loadDB();
  const idx = db.laptops.findIndex(l => l.id === req.params.id && l.user === req.user.id);
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  db.laptops[idx] = { ...db.laptops[idx], ...req.body };
  saveDB(db); 
  res.json(db.laptops[idx]);
});

// TRACKING ENDPOINTS

// Laptop check-in (get location from IP)
app.get('/api/laptops/:id/checkin', async (req, res) => {
  try {
    const db = loadDB();
    const laptop = db.laptops.find(l => l.id === req.params.id);
    if (!laptop) return res.status(404).json({ error: 'Laptop not found' });
    
    // Get IP from request
    const ip = req.headers['x-forwarded-for']?.split(',')[0] || req.connection.remoteAddress;
    
    // Get location from IP using free API
    try {
      const locationRes = await fetch(`http://ip-api.com/json/${ip}`);
      const location = await locationRes.json();
      
      if (location.status === 'success') {
        // Update laptop with location
        const idx = db.laptops.findIndex(l => l.id === req.params.id);
        db.laptops[idx].lastIpAddress = ip;
        db.laptops[idx].lastLocation = {
          city: location.city,
          region: location.regionName,
          country: location.country,
          latitude: location.lat,
          longitude: location.lon,
          timezone: location.timezone
        };
        db.laptops[idx].lastSeen = new Date().toISOString();
        saveDB(db);
        
        return res.json({ 
          message: 'Check-in successful',
          location: db.laptops[idx].lastLocation,
          lastSeen: db.laptops[idx].lastSeen
        });
      }
    } catch (locErr) {
      console.log('Location API error:', locErr);
    }
    
    // If location API fails, just save IP and timestamp
    const idx = db.laptops.findIndex(l => l.id === req.params.id);
    db.laptops[idx].lastIpAddress = ip;
    db.laptops[idx].lastSeen = new Date().toISOString();
    saveDB(db);
    
    res.json({ 
      message: 'Check-in successful (location unavailable)',
      lastSeen: db.laptops[idx].lastSeen
    });
  } catch (err) {
    res.status(500).json({ error: 'Check-in failed: ' + err.message });
  }
});

// Mark laptop as stolen
app.put('/api/laptops/:id/stolen', protect, (req, res) => {
  const db = loadDB();
  const idx = db.laptops.findIndex(l => l.id === req.params.id);
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  
  const laptop = db.laptops[idx];
  if (laptop.user !== req.user.id && !isAdmin(req.user)) {
    return res.status(403).json({ error: 'Not authorized' });
  }
  
  laptop.stolen = req.body.stolen || true;
  laptop.status = req.body.stolen ? 'Stolen' : 'Active';
  if (req.body.stolen) {
    laptop.reportedStolenAt = new Date().toISOString();
    console.log(`🚨 ALERT: Laptop ${laptop.id} marked as STOLEN by user ${req.user.id}`);
    console.log(`Last known location: ${laptop.lastLocation?.city || 'Unknown'}, ${laptop.lastLocation?.country || 'Unknown'}`);
    // TODO: Send email/SMS alerts here
  }
  
  saveDB(db);
  res.json(laptop);
});

// Get laptop location
app.get('/api/laptops/:id/location', protect, (req, res) => {
  const db = loadDB();
  const laptop = db.laptops.find(l => l.id === req.params.id);
  if (!laptop) return res.status(404).json({ error: 'Not found' });
  
  if (laptop.user !== req.user.id && !isAdmin(req.user)) {
    return res.status(403).json({ error: 'Not authorized' });
  }
  
  res.json({
    lastLocation: laptop.lastLocation,
    lastSeen: laptop.lastSeen,
    lastIpAddress: laptop.lastIpAddress,
    stolen: laptop.stolen
  });
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
  res.json(db.laptops.map(l => ({ ...l, ownerName: db.users.find(u => u.id === l.user)?.name || 'Unknown', ownerEmail: db.users.find(u => u.id === l.user)?.email || 'Unknown' })));
});

app.delete('/api/admin/laptops/:id', protect, (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin access required' });
  const db = loadDB();
  db.laptops = db.laptops.filter(l => l.id !== req.params.id);
  saveDB(db); 
  res.json({ message: 'Deleted' });
});

app.get('/api/admin/stolen', protect, (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin access required' });
  const db = loadDB();
  res.json(db.laptops.filter(l => l.stolen).map(l => ({ ...l, ownerName: db.users.find(u => u.id === l.user)?.name || 'Unknown', ownerEmail: db.users.find(u => u.id === l.user)?.email || 'Unknown' })));
});

// FRONTEND ROUTES
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.get('/dashboard', (req, res) => res.sendFile(path.join(__dirname, 'public', 'dashboard.html')));
app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'admin.html')));
app.get('/subscription', (req, res) => res.sendFile(path.join(__dirname, 'public', 'subscription.html')));
app.get('/checkin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'checkin.html')));

app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
