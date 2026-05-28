// 1. Automatically set Trial End Date for new users (21 days from now)
User.pre('save', function(next) {
    if (this.isNew && !this.trialEndDate && this.role !== 'admin') {
        this.trialEndDate = new Date(Date.now() + 21 * 24 * 60 * 60 * 1000);
    }
    next();
});

// 2. Check Trial Status & Send Reminder
const checkTrialStatus = async (user) => {
  if (user.isSubscribed || !user.trialEndDate) return { canAccess: true, message: null };
  
  const today = new Date();
  const trialEnd = new Date(user.trialEndDate);
  const daysLeft = Math.ceil((trialEnd - today) / (1000 * 60 * 60 * 24));
  
  // Send ONE reminder email on Day 21 (Last day of trial)
  if (daysLeft === 21 && !user.trialReminderSent) {
    await sendTrialReminder(user);
    user.trialReminderSent = true;
    await user.save();
  }
  
  // Block access after trial expires
  if (daysLeft < 0) {
    return { canAccess: false, message: 'Your free trial has ended. Please subscribe to continue using Laptop Tracker.' };
  }
  
  return { canAccess: true, daysLeft };
};

// 3. Send Professional Email
const sendTrialReminder = async (user) => {
  const message = `Hi ${user.name},\n\nYour 21-day free trial of Laptop Tracker ends TODAY! 🔔\n\nTo keep your laptop protected with:\n✅ Real-time location tracking\n✅ Theft alerts & notifications\n✅ Location history & recovery tools\n\nPlease subscribe now to continue your protection.\n\nVisit: https://laptop-tracker-2h7l.onrender.com\n\nStay safe,\nThe Laptop Tracker Team`;

  try {
    await transporter.sendMail({
      from: process.env.SMTP_USER,
      to: user.email,
      subject: '⚠️ Your Laptop Tracker Trial Ends Today!',
      text: message
    });
    console.log(`📧 Trial reminder sent to ${user.email}`);
  } catch (err) {
    console.error('❌ Failed to send trial reminder:', err.message);
  }
};

// 4. Middleware to protect routes
const checkTrialMiddleware = async (req, res, next) => {
  if (!req.user) return next();
  
  const trialCheck = await checkTrialStatus(req.user);
  if (!trialCheck.canAccess) {
    return res.status(403).json({ error: trialCheck.message });
  }
  
  if (trialCheck.daysLeft !== undefined) {
    res.locals.trialDaysLeft = trialCheck.daysLeft;
  }
  
  next();
};

// 5. Apply to Laptop Routes
app.use('/api/laptops', authenticateToken, checkTrialMiddleware);
