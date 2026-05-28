require("./trial_logic");
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const crypto = require('crypto');
const { OAuth2Client } = require('google-auth-library');
const axios = require('axios');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const nodemailer = require('nodemailer');
const mongoose = require('mongoose'); // MongoDB Driver

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret';
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@laptoptracker.com';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin232';
const APP_URL = process.env.APP_URL || 'https://laptop-tracker-2h7l.onrender.com';

// 🔌 Connect to MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log(' MongoDB Connected'))
  .catch(err => console.error('❌ MongoDB Error:', err));

// ️ Middleware
app.use(helmet({ contentSecurityPolicy: false, crossOriginEmbedderPolicy: false }));
app.use(cors({ origin: ['https://laptop-tracker-2h7l.onrender.com', 'http://localhost:3000'], credentials: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api/', rateLimit({ windowMs: 60 * 1000, max: 60 }));

const GOOGLE_CLIENT_ID = "725032797775-iam91nooik7abniqg41hjejso90f2asr.apps.googleusercontent.com";
const googleClient = new OAuth2Client(GOOGLE_CLIENT_ID);

// 💰 Payment Configs
const MPESA_CONSUMER_KEY = process.env.MPESA_CONSUMER_KEY;
const MPESA_CONSUMER_SECRET = process.env.MPESA_CONSUMER_SECRET;
const MPESA_SHORTCODE = process.env.MPESA_SHORTCODE;
const MPESA_PASSKEY = process.env.MPESA_PASSKEY;
const MPESA_CALLBACK_URL = process.env.MPESA_CALLBACK_URL;
const MPESA_BASE_URL = process.env.MPESA_BASE_URL;
const pendingPayments = new Map();

const PAYPAL_CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const PAYPAL_SECRET = process.env.PAYPAL_SECRET;
const PAYPAL_BASE_URL = process.env.PAYPAL_BASE_URL || 'https://api-m.sandbox.paypal.com';
const PAYPAL_CURRENCY = process.env.PAYPAL_CURRENCY || 'USD';

// 📧 Email
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST || 'smtp.gmail.com',
  port: parseInt(process.env.SMTP_PORT) || 587,
  secure: false,
  auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS }
});

// ️ Mongoose Models (Database Schemas)
const userSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true, required: true },
  password: String,
  role: { type: String, default: 'user' },
  phone: String,
  verified: { type: Boolean, default: false },
  verificationToken: String,
  trialEndDate: Date,
  trialReminderSent: { type: Boolean, default: false },
  isSubscribed: { type: Boolean, default: false },
  subscriptionExpiryDate: Date,
  provider: { type: String, default: 'local' },
  paymentHistory: [{ amount: Number, currency: String, date: Date, method: String }]
});

const laptopSchema = new mongoose.Schema({
  user: String,
  name: String,
  serial: String,
  status: { type: String, default: 'Active' },
  stolen: { type: Boolean, default: false },
  lastIpAddress: String,
  lastLocation: Object,
  lastSeen: Date
});

const User = mongoose.model('User', userSchema);
const Laptop = mongoose.model('Laptop', laptopSchema);

// 🛡️ Helper: Check Admin
const isAdmin = (user) => user && (user.role === 'admin' || user.email === ADMIN_EMAIL);

// 🔑 Initialize Admin (Only if not exists)
(async () => {
  try {
    const existingAdmin = await User.findOne({ email: ADMIN_EMAIL });
    if (!existingAdmin) {
      const hashed = await bcrypt.hash(ADMIN_PASSWORD, 10);
      await User.create({
        name: 'System Admin',
        email: ADMIN_EMAIL,
        password: hashed,
        role: 'admin',
        verified: true,
        isSubscribed: true,
        subscriptionExpiryDate: new Date('2099-12-31'),
        provider: 'local'
      });
      console.log('👮 Admin account created in MongoDB.');
    }
  } catch (err) { console.error('Admin init error:', err); }
})();

// 📧 Send Confirmation Email
async function sendConfirmationEmail(user) {
  if (!user.email || user.verified) return;
  try {
    const token = crypto.randomBytes(32).toString('hex');
    await User.findByIdAndUpdate(user._id, { verificationToken: token });
    const link = `${APP_URL}/api/auth/confirm?token=${token}`;
    await transporter.sendMail({
      from: `"Laptop Tracker" <${process.env.SMTP_USER}>`,
      to: user.email,
      subject: 'Verify Your Email',
      html: `<div style="font-family:sans-serif;padding:20px;background:#f9fafb;border-radius:10px;"><h2>Welcome! 🚀</h2><p>Hi ${user.name}, click below to verify:</p><a href="${link}" style="padding:10px 20px;background:#2563eb;color:white;text-decoration:none;border-radius:5px;">Verify Email</a></div>`
    });
  } catch (err) { console.error('Email error:', err); }
}

// ==================== AUTH ROUTES ====================

app.post('/api/auth/register', async (req, res) => {
  const { name, email, password } = req.body;
  try {
    const existing = await User.findOne({ email });
    if (existing) return res.status(400).json({ error: 'Email already exists' });
    
    const hashed = await bcrypt.hash(password, 10);
    const trialEndDate = new Date(); trialEndDate.setDate(trialEndDate.getDate() + 21);
    
    const newUser = await User.create({
      name, email, password: hashed, role: 'user', verified: false,
      trialEndDate, isSubscribed: false, provider: 'local'
    });
    
    await sendConfirmationEmail(newUser);
    const token = jwt.sign({ id: newUser._id, role: newUser.role, email: newUser.email }, JWT_SECRET, { expiresIn: '7d' });
    res.status(201).json({ token, user: { id: newUser._id, name, email, role: newUser.role } });
  } catch (err) { res.status(500).json({ error: 'Registration failed' }); }
});

app.post('/api/auth/google', async (req, res) => {
  const { credential } = req.body;
  if (!credential) return res.status(400).json({ error: 'No credential' });
  try {
    const ticket = await googleClient.verifyIdToken({ idToken: credential, audience: GOOGLE_CLIENT_ID });
    const payload = ticket.getPayload();
    let user = await User.findOne({ email: payload.email });
    
    if (!user) {
      const trialEndDate = new Date(); trialEndDate.setDate(trialEndDate.getDate() + 21);
      user = await User.create({
        name: payload.name, email: payload.email, password: 'GOOGLE_USER',
        role: 'user', verified: true, trialEndDate, isSubscribed: false, provider: 'google'
      });
    }
    const token = jwt.sign({ id: user._id, role: user.role, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user._id, name: user.name, email: user.email, role: user.role } });
  } catch { res.status(401).json({ error: 'Invalid Google Token' }); }
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  if (!user) return res.status(400).json({ error: 'Invalid credentials' });
  if (!user.verified && user.provider === 'local') return res.status(403).json({ error: 'Verify email first.' });
  if (!await bcrypt.compare(password, user.password)) return res.status(400).json({ error: 'Invalid credentials' });
  
  const token = jwt.sign({ id: user._id, role: user.role, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
  res.json({ token, user: { id: user._id, name: user.name, email, role: user.role } });
});

app.get('/api/auth/confirm', async (req, res) => {
  const { token } = req.query;
  if (!token) return res.status(400).send('Missing token.');
  try {
    const user = await User.findOne({ verificationToken: token });
    if (!user) return res.status(400).send('Invalid link.');
    user.verified = true; user.verificationToken = null;
    await user.save();
    res.send(`<html><body style="text-align:center;padding:50px;font-family:sans-serif;"><h1>✅ Verified!</h1><a href="/" style="padding:10px 20px;background:#2563eb;color:white;text-decoration:none;border-radius:5px;">Login</a></body></html>`);
  } catch { res.status(500).send('Error.'); }
});

const protect = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Not authorized' });
  try { req.user = jwt.verify(token, JWT_SECRET); next(); }
  catch { res.status(401).json({ error: 'Invalid token' }); }
};

// ==================== PAYPAL ====================
async function getPayPalAccessToken() {
  const auth = Buffer.from(`${PAYPAL_CLIENT_ID}:${PAYPAL_SECRET}`).toString('base64');
  const res = await axios.post(`${PAYPAL_BASE_URL}/v1/oauth2/token`, new URLSearchParams({ grant_type: 'client_credentials' }), {
    headers: { Authorization: `Basic ${auth}`, 'Content-Type': 'application/x-www-form-urlencoded' }
  });
  return res.data.access_token;
}

app.post('/api/paypal/create-order', protect, async (req, res) => {
  try {
    const token = await getPayPalAccessToken();
    const order = { intent: 'CAPTURE', purchase_units: [{ amount: { currency_code: PAYPAL_CURRENCY, value: '20.00' } }] };
    const response = await axios.post(`${PAYPAL_BASE_URL}/v2/checkout/orders`, order, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } });
    res.json({ id: response.data.id });
  } catch (err) { res.status(500).json({ error: 'Failed to create PayPal order' }); }
});

app.post('/api/paypal/capture-order', protect, async (req, res) => {
  const { orderID } = req.body;
  try {
    const token = await getPayPalAccessToken();
    const response = await axios.post(`${PAYPAL_BASE_URL}/v2/checkout/orders/${orderID}/capture`, {}, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } });
    if (response.data.status === 'COMPLETED') {
      const expiry = new Date(); expiry.setMonth(expiry.getMonth() + 4);
      await User.findByIdAndUpdate(req.user.id, {
        isSubscribed: true, subscriptionExpiryDate: expiry,
        $push: { paymentHistory: { amount: 20, currency: 'USD', date: new Date(), method: 'PayPal' } }
      });
      res.json({ status: 'COMPLETED' });
    } else res.status(400).json({ error: 'Payment not completed' });
  } catch (err) { res.status(500).json({ error: 'Capture failed' }); }
});

// ==================== M-PESA ====================
async function getMpesaAccessToken() {
  const auth = Buffer.from(`${MPESA_CONSUMER_KEY}:${MPESA_CONSUMER_SECRET}`).toString('base64');
  const res = await axios.get(`${MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials`, { headers: { Authorization: `Basic ${auth}` } });
  return res.data.access_token;
}
function generateMpesaPassword(timestamp) { return Buffer.from(MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).toString('base64'); }

app.post('/api/mpesa/pay', protect, async (req, res) => {
  try {
    const { phone, amount = 2500 } = req.body;
    if (!phone) return res.status(400).json({ error: 'Phone required' });
    const formattedPhone = phone.replace(/\s/g, '').startsWith('254') ? phone.replace(/\s/g, '') : `254${phone.replace(/^0/, '')}`;
    const token = await getMpesaAccessToken();
    const timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);
    const payload = { BusinessShortCode: MPESA_SHORTCODE, Password: generateMpesaPassword(timestamp), Timestamp: timestamp, TransactionType: "CustomerPayBillOnline", Amount: amount, PartyA: formattedPhone, PartyB: MPESA_SHORTCODE, PhoneNumber: formattedPhone, CallBackURL: MPESA_CALLBACK_URL, AccountReference: "LaptopTracker", TransactionDesc: "Subscription" };
    const stkRes = await axios.post(`${MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest`, payload, { headers: { Authorization: `Bearer ${token}` } });
    pendingPayments.set(formattedPhone, { userId: req.user.id, amount });
    res.json({ message: 'STK Push sent.', CheckoutRequestID: stkRes.data.CheckoutRequestID });
  } catch (err) { res.status(500).json({ error: 'M-Pesa failed' }); }
});

app.post('/api/mpesa/callback', async (req, res) => {
  try {
    const { Body } = req.body; const { stkCallback } = Body;
    res.json({ ResultCode: 0, ResultDesc: 'Success' });
    if (stkCallback.ResultCode === 0) {
      const phone = stkCallback.PhoneNumber;
      const pending = pendingPayments.get(phone);
      if (pending) {
        const expiry = new Date(); expiry.setMonth(expiry.getMonth() + 4);
        await User.findByIdAndUpdate(pending.userId, {
          isSubscribed: true, subscriptionExpiryDate: expiry,
          $push: { paymentHistory: { amount: pending.amount, currency: 'KES', date: new Date(), method: 'M-Pesa' } }
        });
        pendingPayments.delete(phone);
      }
    }
  } catch { res.status(500).json({ ResultCode: 1 }); }
});

// ==================== LAPTOPS & ADMIN ====================
const checkSub = (req, res, next) => {
  User.findById(req.user.id).then(user => {
    if (user && user.role === 'admin') return next();
    const now = new Date();
    const subExpiry = user.subscriptionExpiryDate ? new Date(user.subscriptionExpiryDate) : null;
    const trialEnd = new Date(user.trialEndDate || Date.now());
    if (now < trialEnd) return next();
    if (user.isSubscribed && subExpiry && now < subExpiry) return next();
    res.status(403).json({ error: 'Subscription expired.' });
  });
};

app.post('/api/laptops', protect, checkSub, async (req, res) => {
  const laptop = await Laptop.create({ user: req.user.id, ...req.body, status: 'Active', stolen: false });
  res.status(201).json(laptop);
});
app.get('/api/laptops', protect, async (req, res) => {
  const laptops = await Laptop.find({ user: req.user.id });
  res.json(laptops);
});
app.delete('/api/laptops/:id', protect, async (req, res) => {
  await Laptop.deleteOne({ _id: req.params.id, user: req.user.id });
  res.json({ message: 'Deleted' });
});
app.put('/api/laptops/:id', protect, checkSub, async (req, res) => {
  const laptop = await Laptop.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(laptop);
});
app.get('/api/laptops/:id/checkin', async (req, res) => {
  try {
    const laptop = await Laptop.findById(req.params.id);
    if (!laptop) return res.status(404).json({ error: 'Not found' });
    const ip = req.headers['x-forwarded-for']?.split(',')[0] || req.connection.remoteAddress;
    let loc = { city: 'Unknown', country: 'Unknown', latitude: null, longitude: null, method: 'ip' };
    const { lat, lon } = req.query;
    if (lat && lon) { loc.latitude = parseFloat(lat); loc.longitude = parseFloat(lon); loc.method = 'gps'; loc.city = 'GPS'; loc.country = 'GPS'; }
    else { try { const r = await fetch(`http://ip-api.com/json/${ip}`).then(x=>x.json()); if(r.status==='success'){ loc.city=r.city; loc.country=r.country; loc.latitude=r.lat; loc.longitude=r.lon; loc.method='ip'; }} catch{} }
    
    await Laptop.findByIdAndUpdate(req.params.id, { lastIpAddress: ip, lastLocation: loc, lastSeen: new Date() });
    res.json({ message: 'Checked in', location: loc });
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.put('/api/laptops/:id/stolen', protect, async (req, res) => {
  const laptop = await Laptop.findByIdAndUpdate(req.params.id, { stolen: req.body.stolen || true, status: req.body.stolen ? 'Stolen' : 'Active' }, { new: true });
  res.json(laptop);
});
app.get('/api/laptops/:id/location', protect, async (req, res) => {
  const laptop = await Laptop.findById(req.params.id);
  if (!laptop) return res.status(404).json({ error: 'Not found' });
  res.json({ lastLocation: laptop.lastLocation, lastSeen: laptop.lastSeen, lastIpAddress: laptop.lastIpAddress, stolen: laptop.stolen });
});

app.get('/api/admin/users', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const users = await User.find({}, 'name email role verified isSubscribed subscriptionExpiryDate');
  res.json(users);
});
app.get('/api/admin/laptops', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const laptops = await Laptop.find().populate('user', 'name'); // Note: populate needs ref, simplified here
  res.json(laptops);
});
app.delete('/api/admin/laptops/:id', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  await Laptop.findByIdAndDelete(req.params.id);
  res.json({ message: 'Deleted' });
});
app.get('/api/admin/stolen', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const laptops = await Laptop.find({ stolen: true });
  res.json(laptops);
});

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.get('/dashboard', (req, res) => res.sendFile(path.join(__dirname, 'public', 'dashboard.html')));
app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'admin.html')));
app.get('/subscription', (req, res) => res.sendFile(path.join(__dirname, 'public', 'subscription.html')));
app.get('/checkin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'checkin.html')));

app.listen(PORT, () => console.log(` Server running on port ${PORT}`));
