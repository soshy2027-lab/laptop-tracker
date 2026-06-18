with open('public/dashboard.html', 'r') as f:
    content = f.read()

old_data = """const data = {
        brand: document.getElementById('brand').value,"""
new_data = """const data = {
        deviceType: document.getElementById('deviceType').value,
        brand: document.getElementById('brand').value,"""

if old_data in content:
    content = content.replace(old_data, new_data)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Fixed! The form will now send 'Phone' to the database.")
else:
    print("❌ Could not find the exact code.")
