with open('server.js', 'r') as f:
    server = f.read()

old_stolen = """app.get('/api/admin/stolen', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const laptops = await Laptop.find({ stolen: true });
  res.json(laptops);
});"""

new_stolen = """app.get('/api/admin/stolen', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const laptops = await Laptop.find({ stolen: true });
  res.json(laptops);
});

app.get('/api/admin/user/:id', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const user = await User.findById(req.params.id).select('name email');
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});"""

server = server.replace(old_stolen, new_stolen)

with open('server.js', 'w') as f:
    f.write(server)

print("✅ Added user endpoint!")
