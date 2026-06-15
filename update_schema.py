with open('server.js', 'r') as f:
    content = f.read()

old_schema = """const laptopSchema = new mongoose.Schema({
  user: String, name: String, serial: String, brand: String, model: String, ram: String, storage: String,
  status: { type: String, default: 'Active' }, stolen: { type: Boolean, default: false },
  lastIpAddress: String, lastLocation: Object, lastSeen: Date
});"""

new_schema = """const laptopSchema = new mongoose.Schema({
  user: String, name: String, serial: String, brand: String, model: String, ram: String, storage: String,
  status: { type: String, default: 'Active' }, stolen: { type: Boolean, default: false },
  obNumber: String, policeStation: String, reportDate: Date,
  lastIpAddress: String, lastLocation: Object, lastSeen: Date
});"""

if old_schema in content:
    content = content.replace(old_schema, new_schema)
    with open('server.js', 'w') as f:
        f.write(content)
    print("Schema updated successfully!")
else:
    print("Could not find schema to replace!")
