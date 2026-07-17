with open('server.js', 'r') as f:
    server_code = f.read()

# Add console.log statements to debug
old_code = """app.post('/api/admin/send-reminders', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });

  try {
    const twoDaysAgo = new Date();
    twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);

    // Find users whose trial ended more than 2 days ago and haven't subscribed
    const expiredUsers = await User.find({
      isSubscribed: false,
      subscriptionExpiryDate: { $lte: twoDaysAgo },
      email: { $ne: process.env.ADMIN_EMAIL }
    });"""

new_code = """app.post('/api/admin/send-reminders', protect, async (req, res) => {
  console.log('📧 Email reminder endpoint called');
  console.log('User email:', req.user?.email);
  console.log('Is admin:', isAdmin(req.user));
  
  if (!isAdmin(req.user)) {
    console.log('❌ Not admin, rejecting');
    return res.status(403).json({ error: 'Admin only' });
  }

  try {
    const twoDaysAgo = new Date();
    twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);
    console.log('Looking for users expired since:', twoDaysAgo);

    // Find users whose trial ended more than 2 days ago and haven't subscribed
    const expiredUsers = await User.find({
      isSubscribed: false,
      subscriptionExpiryDate: { $lte: twoDaysAgo },
      email: { $ne: process.env.ADMIN_EMAIL }
    });
    
    console.log('Found', expiredUsers.length, 'expired users');"""

server_code = server_code.replace(old_code, new_code)

with open('server.js', 'w') as f:
    f.write(server_code)

print("✅ Added debug logs!")
