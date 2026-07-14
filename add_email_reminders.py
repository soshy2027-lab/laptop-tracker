import re

# 1. Update Admin Dashboard to add the button
with open('public/admin.html', 'r') as f:
    admin_html = f.read()

# Add button near the top of the admin dashboard
button_html = """
<div style="margin: 20px 0; text-align: center;">
  <button onclick="sendReminders()" style="background: #10b981; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer;">
    📧 Send Trial Expiry Reminders (Twice a Week)
  </button>
</div>
<script>
  async function sendReminders() {
    if (!confirm('Send email reminders to all users with expired trials?')) return;
    try {
      const res = await fetch('/api/admin/send-reminders', { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } });
      const data = await res.json();
      alert(data.message || 'Reminders sent!');
    } catch (err) { alert('Error sending reminders'); }
  }
</script>
"""
# Insert after the logout button or header
if 'Send Trial Expiry Reminders' not in admin_html:
    admin_html = admin_html.replace('<div class="header">', button_html + '\n<div class="header">')
    with open('public/admin.html', 'w') as f:
        f.write(admin_html)

# 2. Safely add the endpoint to the very bottom of server.js
with open('server.js', 'r') as f:
    server_code = f.read()

new_endpoint = """
// --- EMAIL REMINDERS ENDPOINT ---
app.post('/api/admin/send-reminders', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  
  try {
    const twoDaysAgo = new Date();
    twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);
    
    // Find users whose trial ended more than 2 days ago and haven't subscribed
    const expiredUsers = await User.find({
      isSubscribed: false,
      subscriptionExpiryDate: { $lte: twoDaysAgo },
      email: { $ne: process.env.ADMIN_EMAIL }
    });
    
    let sentCount = 0;
    for (const user of expiredUsers) {
      try {
        await resend.emails.send({
          from: process.env.FROM_EMAIL || 'onboarding@resend.dev',
          to: user.email,
          subject: '⚠️ Your Laptop Tracker Trial Has Expired',
          html: `
            <h2>Hello ${user.name || 'User'},</h2>
            <p>Your 21-day free trial for <strong>Laptop Tracker</strong> has ended.</p>
            <p style="background: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin: 20px 0;">
              <strong>⚠️ Important:</strong> Without an active subscription, you cannot track stolen devices or access premium features.
            </p>
            <p>Don't leave your device unprotected! Subscribe now to continue protecting your laptop and phone.</p>
            <a href="${process.env.APP_URL || 'https://laptop-tracker-2h7l.onrender.com'}/subscription" 
               style="display: inline-block; background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin: 10px 0;">
              Subscribe Now
            </a>
          `
        });
        sentCount++;
      } catch (err) {
        console.error(`Failed to send to ${user.email}:`, err.message);
      }
    }
    
    res.json({ message: `✅ Sent ${sentCount} reminder emails successfully.` });
  } catch (err) {
    res.status(500).json({ error: 'Failed to send reminders' });
  }
});
"""

# Only add if it doesn't exist yet
if '// --- EMAIL REMINDERS ENDPOINT ---' not in server_code:
    server_code += new_endpoint
    with open('server.js', 'w') as f:
        f.write(server_code)

print("✅ Email reminder system added safely!")
