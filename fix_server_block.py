import re

with open('server.js', 'r') as f:
    content = f.read()

# Find the broken checkSub function
pattern = r"const checkSub = \(req, res, next\) => \{[\s\S]*?res\.status\(403\)\.json\(\{ error: 'Subscription expired\.' \}\);\s*\}\);\s*\};"

# Replace it with a safe version that handles missing dates
new_func = """const checkSub = (req, res, next) => {
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
};"""

if re.search(pattern, content):
    content = re.sub(pattern, new_func, content)
    with open('server.js', 'w') as f:
        f.write(content)
    print("✅ Fixed subscription check! You can now add devices again.")
else:
    print("❌ Could not find the checkSub function.")
