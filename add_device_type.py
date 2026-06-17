with open('server.js', 'r') as f:
    content = f.read()

# We are only adding one tiny label: deviceType
old_line = "  user: String, name: String, serial: String, brand: String, model: String, ram: String, storage: String,"
new_line = "  user: String, deviceType: { type: String, default: 'Laptop' }, name: String, serial: String, brand: String, model: String, ram: String, storage: String,"

if old_line in content:
    content = content.replace(old_line, new_line)
    with open('server.js', 'w') as f:
        f.write(content)
    print("✅ Added deviceType label safely! Old laptops are untouched.")
else:
    print("❌ Could not find the exact line. Let me know!")
