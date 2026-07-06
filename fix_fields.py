import re

# 1. Fix server.js to manually match user names
with open('server.js', 'r') as f:
    server = f.read()

pattern = r"app\.get\('/api/admin/laptops',\s*protect,\s*async\s*\(req,\s*res\)\s*=>\s*\{[\s\S]*?res\.json\(.*?\);\s*\}\);"
replacement = """app.get('/api/admin/laptops', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const laptops = await Laptop.find();
  const userIds = [...new Set(laptops.map(l => l.user).filter(Boolean))];
  const users = await User.find({ _id: { $in: userIds } }).select('name');
  const userMap = {};
  users.forEach(u => { userMap[String(u._id)] = u.name; });
  const result = laptops.map(l => ({ ...l.toObject(), ownerName: userMap[String(l.user)] || 'Unknown' }));
  res.json(result);
});"""

server = re.sub(pattern, replacement, server)

with open('server.js', 'w') as f:
    f.write(server)

# 2. Fix admin.html to use the correct field name 'serial'
with open('public/admin.html', 'r') as f:
    html = f.read()

html = html.replace('l.serialNumber', 'l.serial')
html = html.replace("l.user?.name || 'Unknown'", "l.ownerName || 'Unknown'")

with open('public/admin.html', 'w') as f:
    f.write(html)

print("✅ Fixed field names and owner mapping!")
