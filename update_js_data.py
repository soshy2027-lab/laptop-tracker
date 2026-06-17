with open('public/dashboard.html', 'r') as f:
    content = f.read()

old_data = """      const data = {
        brand: document.getElementById('brand').value,"""

new_data = """      const data = {
        deviceType: document.getElementById('deviceType').value,
        brand: document.getElementById('brand').value,"""

if old_data in content:
    content = content.replace(old_data, new_data, 1)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ JavaScript updated safely! The form will now send the device type.")
else:
    print("❌ Could not find the data block. Please run: sed -n '459,463p' public/dashboard.html and reply with the output.")
