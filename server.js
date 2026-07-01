require('dotenv').config();
const { Resend } = require('resend');
const resend = new Resend(process.env.RESEND_API_KEY);
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
const mongoose = require('mongoose');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret';
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@laptoptracker.com';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin232';
const APP_URL = process.env.APP_URL || 'https://laptop-tracker-2h7l.onrender.com';

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.error('MongoDB Error:', err));

app.use(helmet({ contentSecurityPolicy: false, crossOriginEmbedderPolicy: false }));
app.use(cors({ origin: ['https://laptop-tracker-2h7l.onrender.com', 'http://localhost:3000'], credentials: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api/', rateLimit({ windowMs: 60 * 1000, max: 60 }));

const GOOGLE_CLIENT_ID = "725032797775-iam91nooik7abniqg41hjejso90f2asr.apps.googleusercontent.com";
const googleClient = new OAuth2Client(GOOGLE_CLIENT_ID);

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

const userSchema = new mongoose.Schema({
  name: String, email: { type: String, unique: true, required: true }, password: String,
  role: { type: String, default: 'user' }, phone: String, verified: { type: Boolean, default: false },
  verificationToken: String, subscriptionExpiryDate: Date, trialReminderSent: { type: Boolean, default: false },
  isSubscribed: { type: Boolean, default: false }, subscriptionExpiryDate: Date,
  provider: { type: String, default: 'local' },
  paymentHistory: [{ amount: Number, currency: String, date: Date, method: String }]
});

const laptopSchema = new mongoose.Schema({
  user: String, deviceType: { type: String, default: 'Laptop' }, name: String, serial: String, brand: String, model: String, ram: String, storage: String,
  status: { type: String, default: 'Active' }, stolen: { type: Boolean, default: false },
  obNumber: String, policeStation: String, reportDate: Date,
  lastIpAddress: String, lastLocation: Object, lastSeen: Date
});

const User = mongoose.model('User', userSchema);
const Laptop = mongoose.model('Laptop', laptopSchema);

const isAdmin = (user) => user && (user.role === 'admin' || user.email === ADMIN_EMAIL);

(async () => {
  try {
    const existingAdmin = await User.findOne({ email: ADMIN_EMAIL });
    if (!existingAdmin) {
      const hashed = await bcrypt.hash(ADMIN_PASSWORD, 10);
      await User.create({ name: 'System Admin', email: ADMIN_EMAIL, password: hashed, role: 'admin', verified: true, isSubscribed: true, subscriptionExpiryDate: new Date('2099-12-31'), provider: 'local' });
      console.log('Admin account created.');
    }
  } catch (err) { console.error('Admin init error:', err); }
})();

async function sendConfirmationEmail(user) {
  if (!user.email || user.verified) return;
  try {
    const token = crypto.randomBytes(32).toString('hex');
    await User.findByIdAndUpdate(user._id, { verificationToken: token });
    const link = APP_URL + '/api/auth/confirm?token=' + token;
    
    const htmlContent = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">' +
      '<h1 style="color: #2563eb; text-align: center;">🎉 Welcome to Laptop Tracker!</h1>' +
      '<div style="background: #f0fdf4; border: 2px solid #16a34a; padding: 15px; border-radius: 8px; margin: 20px 0;">' +
        '<h2 style="color: #15803d; margin: 0;">✅ Your Account is Created!</h2>' +
        '<p style="margin: 10px 0 0 0; font-size: 16px;"><strong>You have 21 Days FREE Trial</strong> - Full access, no credit card required!</p>' +
      '</div>' +
      '<h3>📧 Verify Your Email</h3>' +
      '<p>Click the button below to verify your email address:</p>' +
      '<a href="' + link + '" style="display: inline-block; background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 10px 0;">Verify Email Address</a>' +
      '<h3>💻 Next Steps</h3>' +
      '<ol style="line-height: 1.8;">' +
        '<li>Verify your email using the button above</li>' +
        '<li>Open this website on your <strong>LAPTOP</strong> computer</li>' +
        '<li>Log in and click "Open Tracker Page"</li>' +
        '<li>Keep the tracker running to track your device</li>' +
      '</ol>' +
      '<p style="color: #6b7280; font-size: 14px; margin-top: 30px;">If you did not create this account, please ignore this email.</p>' +
    '</div>';
    
    await resend.emails.send({ 
      from: process.env.FROM_EMAIL || 'onboarding@resend.dev', 
      to: user.email, 
      subject: '🎉 Welcome! Verify Your Email & Start 21-Day Free Trial', 
      html: htmlContent 
    });
    console.log('✅ Welcome email sent to:', user.email);
  } catch (err) { 
    console.error('❌ Email error:', err); 
  }
}


app.post('/api/auth/register', async (req, res) => {
  const { name, email, password } = req.body;
  try {
    const existing = await User.findOne({ email });
    if (existing) return res.status(400).json({ error: 'Email already exists' });
    const hashed = await bcrypt.hash(password, 10);
    const subscriptionExpiryDate = new Date(); subscriptionExpiryDate.setDate(subscriptionExpiryDate.getDate() + 21);
    const newUser = await User.create({ name, email, password: hashed, role: 'user', verified: false, subscriptionExpiryDate, isSubscribed: false, provider: 'local' });
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
      const subscriptionExpiryDate = new Date(); subscriptionExpiryDate.setDate(subscriptionExpiryDate.getDate() + 21);
      user = await User.create({ name: payload.name, email: payload.email, password: 'GOOGLE_USER', role: 'user', verified: true, subscriptionExpiryDate, isSubscribed: false, provider: 'google' });
    }
    const token = jwt.sign({ id: user._id, role: user.role, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user._id, name: user.name, email: user.email, role: user.role } });
  } catch { res.status(401).json({ error: 'Invalid Google Token' }); }
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  if (!user) return res.status(400).json({ error: 'Invalid credentials' });
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
    res.send('<html><body style="text-align:center;padding:50px;font-family:sans-serif;"><h1>Verified!</h1><a href="/" style="padding:10px 20px;background:#2563eb;color:white;text-decoration:none;border-radius:5px;">Login</a></body></html>');
  } catch { res.status(500).send('Error.'); }
});

const protect = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Not authorized' });
  try { req.user = jwt.verify(token, JWT_SECRET); next(); }
  catch { res.status(401).json({ error: 'Invalid token' }); }
};

async function getPayPalAccessToken() {
  const auth = Buffer.from(PAYPAL_CLIENT_ID + ':' + PAYPAL_SECRET).toString('base64');
  const res = await axios.post(PAYPAL_BASE_URL + '/v1/oauth2/token', new URLSearchParams({ grant_type: 'client_credentials' }), { headers: { Authorization: 'Basic ' + auth, 'Content-Type': 'application/x-www-form-urlencoded' } });
  return res.data.access_token;
}

app.post('/api/paypal/create-order', protect, async (req, res) => {
  try {
    const token = await getPayPalAccessToken();
    const order = { intent: 'CAPTURE', purchase_units: [{ amount: { currency_code: PAYPAL_CURRENCY, value: '20.00' } }] };
    const response = await axios.post(PAYPAL_BASE_URL + '/v2/checkout/orders', order, { headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' } });
    res.json({ id: response.data.id });
  } catch (err) { res.status(500).json({ error: 'Failed to create PayPal order' }); }
});

app.post('/api/paypal/capture-order', protect, async (req, res) => {
  const { orderID } = req.body;
  try {
    const token = await getPayPalAccessToken();
    const response = await axios.post(PAYPAL_BASE_URL + '/v2/checkout/orders/' + orderID + '/capture', {}, { headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' } });
    if (response.data.status === 'COMPLETED') {
      const expiry = new Date(); expiry.setMonth(expiry.getMonth() + 4);
      await User.findByIdAndUpdate(req.user.id, { isSubscribed: true, subscriptionExpiryDate: expiry, $push: { paymentHistory: { amount: 20, currency: 'USD', date: new Date(), method: 'PayPal' } } });
      res.json({ status: 'COMPLETED' });
    } else res.status(400).json({ error: 'Payment not completed' });
  } catch (err) { res.status(500).json({ error: 'Capture failed' }); }
});

async function getMpesaAccessToken() {
  const auth = Buffer.from(MPESA_CONSUMER_KEY + ':' + MPESA_CONSUMER_SECRET).toString('base64');
  const res = await axios.get(MPESA_BASE_URL + '/oauth/v1/generate?grant_type=client_credentials', { headers: { Authorization: 'Basic ' + auth } });
  return res.data.access_token;
}
function generateMpesaPassword(timestamp) { return Buffer.from(MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).toString('base64'); }

app.post('/api/mpesa/pay', protect, async (req, res) => {
  try {
    const { phone, amount = 2500 } = req.body;
    if (!phone) return res.status(400).json({ error: 'Phone required' });
    const formattedPhone = phone.replace(/\s/g, '').startsWith('254') ? phone.replace(/\s/g, '') : '254' + phone.replace(/^0/, '');
    const token = await getMpesaAccessToken();
    const timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);
    const payload = { BusinessShortCode: MPESA_SHORTCODE, Password: generateMpesaPassword(timestamp), Timestamp: timestamp, TransactionType: "CustomerPayBillOnline", Amount: amount, PartyA: formattedPhone, PartyB: MPESA_SHORTCODE, PhoneNumber: formattedPhone, CallBackURL: MPESA_CALLBACK_URL, AccountReference: "LaptopTracker", TransactionDesc: "Subscription" };
    const stkRes = await axios.post(MPESA_BASE_URL + '/mpesa/stkpush/v1/processrequest', payload, { headers: { Authorization: 'Bearer ' + token } });
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
        await User.findByIdAndUpdate(pending.userId, { isSubscribed: true, subscriptionExpiryDate: expiry, $push: { paymentHistory: { amount: pending.amount, currency: 'KES', date: new Date(), method: 'M-Pesa' } } });
        pendingPayments.delete(phone);
      }
    }
  } catch { res.status(500).json({ ResultCode: 1 }); }
});

const checkSub = (req, res, next) => {
  User.findById(req.user.id).then(async user => {
    if (user && user.role === 'admin') return next();
    const now = new Date();
    // If no expiry date exists (legacy users), give them a 21-day trial and save it
    if (!user.subscriptionExpiryDate) {
      const trialEnd = new Date();
      trialEnd.setDate(trialEnd.getDate() + 21);
      user.subscriptionExpiryDate = trialEnd;
      await user.save();
      return next();
    }
    const subExpiry = new Date(user.subscriptionExpiryDate);
    if (now < subExpiry) return next();
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
    else { try { const r = await fetch('http://ip-api.com/json/' + ip).then(x=>x.json()); if(r.status==='success'){ loc.city=r.city; loc.country=r.country; loc.latitude=r.lat; loc.longitude=r.lon; loc.method='ip'; }} catch{} }
    await Laptop.findByIdAndUpdate(req.params.id, { lastIpAddress: ip, lastLocation: loc, lastSeen: new Date() });
    res.json({ message: 'Checked in', location: loc });
  } catch (err) { res.status(500).json({ error: err.message }); }
});

app.put('/api/laptops/:id/stolen', protect, async (req, res) => {
  const updateData = { 
    stolen: req.body.stolen, 
    status: req.body.stolen ? 'Stolen' : 'Active',
    obNumber: req.body.obNumber || '',
    policeStation: req.body.policeStation || '',
    reportDate: req.body.reportDate || null
  };
  const laptop = await Laptop.findByIdAndUpdate(req.params.id, updateData, { new: true });
  if (req.body.stolen && req.user?.email) {
    const location = laptop.lastLocation?.city ? laptop.lastLocation.city + ', ' + laptop.lastLocation.country : 'Unknown';
    const mapUrl = laptop.lastLocation?.latitude ? 'https://maps.google.com?q=' + laptop.lastLocation.latitude + ',' + laptop.lastLocation.longitude : '#';
    try {
      await resend.emails.send({ from: process.env.FROM_EMAIL || 'onboarding@resend.dev', to: ADMIN_EMAIL, subject: 'STOLEN LAPTOP ALERT', html: '<h2>Stolen Laptop Reported</h2><p>User: ' + req.user.email + '</p><p>Laptop: ' + (laptop.brand || '') + ' ' + (laptop.model || '') + ' | Serial: ' + laptop.serial + '</p><p><strong>OB Number:</strong> ' + (laptop.obNumber || 'Not provided') + '</p><p><strong>Police Station:</strong> ' + (laptop.policeStation || 'Not provided') + '</p><p><strong>Report Date:</strong> ' + (laptop.reportDate ? new Date(laptop.reportDate).toLocaleDateString() : 'Not provided') + '</p><p>Location: ' + location + '</p><p><a href="' + mapUrl + '">View on Map</a></p>' });
      await resend.emails.send({ from: process.env.FROM_EMAIL || 'onboarding@resend.dev', to: req.user.email, subject: 'Your Laptop Marked as Stolen', html: '<h2>Laptop Marked as Stolen</h2><p>Your laptop ' + (laptop.brand || '') + ' ' + (laptop.model || '') + ' (Serial: ' + laptop.serial + ') has been marked as stolen.</p><p><strong>OB Number:</strong> ' + (laptop.obNumber || 'Not provided') + '</p><p><strong>Police Station:</strong> ' + (laptop.policeStation || 'Not provided') + '</p><p><strong>Report Date:</strong> ' + (laptop.reportDate ? new Date(laptop.reportDate).toLocaleDateString() : 'Not provided') + '</p><p>Location: ' + location + '</p><p><a href="' + mapUrl + '">View Location</a></p>' });
    } catch (err) { console.error('Email error:', err); }
  }
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
  const laptops = await Laptop.find();
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


// Contact Form Route
app.post('/api/contact', async (req, res) => {
  const { name, email, subject, message } = req.body;
  if (!name || !email || !subject || !message) {
    return res.status(400).json({ error: 'All fields are required' });
  }
  try {
    await resend.emails.send({
      from: process.env.FROM_EMAIL || 'onboarding@resend.dev',
      to: ADMIN_EMAIL || 'support@laptoptracker.com',
      subject: 'Contact Form: ' + subject + ' (from ' + name + ')',
      html: '<h2>New Contact Form Submission</h2><p><strong>Name:</strong> ' + name + '</p><p><strong>Email:</strong> ' + email + '</p><p><strong>Subject:</strong> ' + subject + '</p><p><strong>Message:</strong><br>' + message.replace(/\n/g, '<br>') + '</p>'
    });
    res.json({ message: 'Email sent successfully' });
  } catch (err) {
    console.error('Contact email error:', err);
    res.status(500).json({ error: 'Failed to send email' });
  }
});

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.get('/dashboard', (req, res) => res.sendFile(path.join(__dirname, 'public', 'dashboard.html')));
app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'admin.html')));
app.get('/subscription', (req, res) => res.sendFile(path.join(__dirname, 'public', 'subscription.html')));
app.get('/checkin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'checkin.html')));

const sendTrialReminders = async () => {
  try {
    const users = await User.find({ isSubscribed: false, subscriptionExpiryDate: { $exists: true } });
    const today = new Date();
    for (const user of users) {
      const daysLeft = Math.ceil((new Date(user.subscriptionExpiryDate) - today) / (1000 * 60 * 60 * 24));
      if ([21, 18, 1].includes(daysLeft) && !user.trialReminderSent) {
        const subject = daysLeft === 1 ? 'Trial Ends Tomorrow!' : daysLeft + ' Days Left in Trial';
        await resend.emails.send({ from: process.env.FROM_EMAIL || 'onboarding@resend.dev', to: user.email, subject: subject, html: '<p>Hi ' + user.name + ', your trial ends in ' + daysLeft + ' days. Subscribe: https://laptop-tracker-2h7l.onrender.com</p>' });
        user.trialReminderSent = true;
        await user.save();
      }
    }
  } catch (err) { console.log('Trial reminder error:', err.message); }
};
setInterval(sendTrialReminders, 6 * 60 * 60 * 1000);
setTimeout(sendTrialReminders, 5000);

// ==================== FORGOT PASSWORD ROUTES ====================
app.post('/api/auth/forgot-password', async (req, res) => {
  const { email } = req.body;
  try {
    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ error: 'User not found' });

    const resetToken = crypto.randomBytes(32).toString('hex');
    user.verificationToken = resetToken;
    await user.save();

    const resetLink = APP_URL + '/reset-password?token=' + resetToken;

    await resend.emails.send({
      from: process.env.FROM_EMAIL || 'onboarding@resend.dev',
      to: user.email,
      subject: 'Password Reset Request',
      html: '<h2>Password Reset</h2><p>Click the link below to reset your password. This link expires in 1 hour.</p><p><a href="' + resetLink + '">Reset Password</a></p>'
    });

    res.json({ message: 'Password reset link sent to your email.' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/auth/reset-password', async (req, res) => {
  const { token, newPassword } = req.body;
  try {
    const user = await User.findOne({ verificationToken: token });
    if (!user) return res.status(400).json({ error: 'Invalid or expired token' });

    const hashed = await bcrypt.hash(newPassword, 10);
    user.password = hashed;
    user.verificationToken = null;
    await user.save();

    res.json({ message: 'Password reset successfully.' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});


// Profile Route

// JWT Verification Middleware
const verifyToken = (req, res, next) => {
  const token = req.headers['authorization']?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token provided' });
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Profile API Endpoint
app.get('/api/auth/profile', verifyToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.id).select('-password');
    if (!user) return res.status(404).json({ error: 'User not found' });
    
    res.json({
      name: user.name,
      email: user.email,
      phone: user.phone || 'Not provided',
      memberSince: user.createdAt || new Date(),
      subscriptionExpiryDate: user.subscriptionExpiryDate,
      isSubscribed: user.isSubscribed,
      subscriptionExpiryDate: user.subscriptionExpiryDate
    });
  } catch (err) {
    console.error('Profile fetch error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.get('/profile', (req, res) => {
  res.sendFile(__dirname + '/public/profile.html');
});

app.listen(PORT, () => console.log('Server running on port ' + PORT));
// --- PESAPAL INTEGRATION ---
const PESAPAL_CONSUMER_KEY = process.env.PESAPAL_CONSUMER_KEY;
const PESAPAL_CONSUMER_SECRET = process.env.PESAPAL_CONSUMER_SECRET;
const PESAPAL_BASE_URL = 'https://pay.pesapal.com/v3';

async function getPesapalToken() {
  const res = await axios.post(`${PESAPAL_BASE_URL}/api/Auth/RequestToken`, {
    consumer_key: PESAPAL_CONSUMER_KEY,
    consumer_secret: PESAPAL_CONSUMER_SECRET
  });
  return res.data.token;
}

app.post('/api/pesapal/submit-order', protect, async (req, res) => {
  try {
    console.log('=== PESAPAL REQUEST STARTED ===');
    console.log('User ID:', req.user._id);
    console.log('Consumer Key:', PESAPAL_CONSUMER_KEY);
    console.log('Base URL:', PESAPAL_BASE_URL);
    
    const token = await getPesapalToken();
    console.log('✅ Got Pesapal token');
    const orderData = {
      id: 'LAPTOP_' + Date.now(),
      currency_code: 'KES',
      amount: 2500.00,
      description: 'Laptop Tracker Subscription - 4 Months',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      notification_id: '',
      ordering_reference: 'LAPTOP_' + Date.now(),
      meta_data: [],
      items: [
        {
          title: 'Laptop Tracker Subscription',
          description: '4 months unlimited tracking',
          unit_cost: 2500.00,
          quantity: 1,
          sku_code: 'LAPTOP_SUB_4M',
          tax: 0.00
        }
      ]
    };
    console.log('Sending order to Pesapal...');
    console.log('Order data:', JSON.stringify(orderData, null, 2));
    
    const response = await axios.post(`${PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest`, orderData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json', Accept: 'application/json' }
    });
    
    console.log('✅ Pesapal response:', response.data);
    res.json({ redirect_url: response.data.RedirectURL });
  } catch (err) {
    console.log('❌ PESAPAL ERROR:', err.message);
    console.log('❌ Error details:', err.response?.data);
    console.log('❌ Error status:', err.response?.status);
    res.status(500).json({ 
      error: 'Pesapal failed', 
      details: err.response?.data || err.message,
      status: err.response?.status 
    });
  }
});
// --- END PESAPAL ---
