with open('server.js', 'r') as f:
    content = f.read()

# Find the broken email function and replace it with string concatenation
old_broken = """async function sendConfirmationEmail(user) {
  if (!user.email || user.verified) return;
  try {
    const token = crypto.randomBytes(32).toString('hex');
    await User.findByIdAndUpdate(user._id, { verificationToken: token });
    const link = APP_URL + '/api/auth/confirm?token=' + token;
    
    const htmlContent = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2563eb; text-align: center;">🎉 Welcome to Laptop Tracker!</h1>
        <div style="background: #f0fdf4; border: 2px solid #16a34a; padding: 15px; border-radius: 8px; margin: 20px 0;">
          <h2 style="color: #15803d; margin: 0;"> ✅ Your Account is Created!</h2>
          <p style="margin: 10px 0 0 0; font-size: 16px;"><strong>You have 21 Days FREE Trial</strong> - Full access, no credit card required!</p>
        </div>
        <h3>📧 Verify Your Email</h3>
        <p>Click the button below to verify your email address:</p>
        <a href="${link}" style="display: inline-block; background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 10px 0;">Verify Email Address</a>
        <h3>💻 Next Steps</h3>
        <ol style="line-height: 1.8;">
          <li>Verify your email using the button above</li>
          <li>Open this website on your <strong>LAPTOP</strong> computer</li>
          <li>Log in and click "Open Tracker Page"</li>
          <li>Keep the tracker running to track your device</li>
        </ol>
        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">If you didn't create this account, please ignore this email.</p>
      </div>
    `;
    
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
}"""

new_fixed = """async function sendConfirmationEmail(user) {
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
      '<p style="color: #6b7280; font-size: 14px; margin-top: 30px;">If you didn\'t create this account, please ignore this email.</p>' +
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
}"""

if old_broken in content:
    content = content.replace(old_broken, new_fixed)
    with open('server.js', 'w') as f:
        f.write(content)
    print("✅ Fixed email syntax - using string concatenation!")
else:
    print("❌ Could not find the broken code. Run: grep -n 'const htmlContent' server.js and reply with output")
