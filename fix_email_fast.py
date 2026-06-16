with open('server.js', 'r') as f:
    lines = f.readlines()

# Find and replace the broken email function
new_function = """async function sendConfirmationEmail(user) {
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
"""

# Find the start and end of the function
start_idx = None
end_idx = None
brace_count = 0
in_function = False

for i, line in enumerate(lines):
    if 'async function sendConfirmationEmail' in line:
        start_idx = i
        in_function = True
        brace_count = 0
    
    if in_function:
        brace_count += line.count('{') - line.count('}')
        if brace_count == 0 and '{' in ''.join(lines[start_idx:i+1]):
            end_idx = i
            break

if start_idx is not None and end_idx is not None:
    lines = lines[:start_idx] + [new_function + '\n'] + lines[end_idx+1:]
    with open('server.js', 'w') as f:
        f.writelines(lines)
    print("✅ Email function fixed!")
else:
    print("❌ Could not find function")
