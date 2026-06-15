with open('server.js', 'r') as f:
    content = f.read()

old_route = """app.put('/api/laptops/:id/stolen', protect, async (req, res) => {
  const laptop = await Laptop.findByIdAndUpdate(req.params.id, { stolen: req.body.stolen, status: req.body.stolen ? 'Stolen' : 'Active' }, { new: true });"""

new_route = """app.put('/api/laptops/:id/stolen', protect, async (req, res) => {
  const updateData = { 
    stolen: req.body.stolen, 
    status: req.body.stolen ? 'Stolen' : 'Active',
    obNumber: req.body.obNumber || '',
    policeStation: req.body.policeStation || '',
    reportDate: req.body.reportDate || null
  };
  const laptop = await Laptop.findByIdAndUpdate(req.params.id, updateData, { new: true });"""

if old_route in content:
    content = content.replace(old_route, new_route)
    with open('server.js', 'w') as f:
        f.write(content)
    print("Route updated successfully!")
else:
    print("Could not find route to replace!")
