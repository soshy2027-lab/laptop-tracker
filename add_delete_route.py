with open('server.js', 'r') as f:
    server = f.read()

# The exact code we want to insert our new route after
target = """app.get('/api/admin/user/:id', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  const user = await User.findById(req.params.id).select('name email');
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});"""

# The new delete route we want to add
addition = """

app.delete('/api/admin/user/:id', protect, async (req, res) => {
  if (!isAdmin(req.user)) return res.status(403).json({ error: 'Admin only' });
  await User.findByIdAndDelete(req.params.id);
  await Laptop.deleteMany({ user: req.params.id });
  res.json({ message: 'User and their laptops deleted successfully' });
});"""

if target in server:
    server = server.replace(target, target + addition)
    with open('server.js', 'w') as f:
        f.write(server)
    print("✅ Delete endpoint added successfully!")
else:
    print("❌ Could not find the target code. Please check server.js")
