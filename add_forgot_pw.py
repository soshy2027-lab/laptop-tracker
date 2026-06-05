with open('server.js', 'r') as f:
    code = f.read()

new_routes = """
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
"""

code = code.replace("app.listen(PORT,", new_routes + "\napp.listen(PORT,")

with open('server.js', 'w') as f:
    f.write(code)
print("Routes added successfully!")
