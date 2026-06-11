with open('server.js', 'r') as f:
    content = f.read()

# Add JWT verification middleware and profile endpoint
profile_api = """
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
      trialEndDate: user.trialEndDate,
      isSubscribed: user.isSubscribed,
      subscriptionExpiryDate: user.subscriptionExpiryDate
    });
  } catch (err) {
    console.error('Profile fetch error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});
"""

# Insert before the profile route
if "app.get('/profile'" in content and 'verifyToken' not in content:
    content = content.replace("app.get('/profile'", profile_api + "\napp.get('/profile'")
    with open('server.js', 'w') as f:
        f.write(content)
    print("Profile API added successfully!")
else:
    print("Profile route not found or already exists!")
