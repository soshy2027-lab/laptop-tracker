with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Update tracker box title
content = content.replace('Auto-Tracker for Your Laptop', 'Auto-Tracker for Your Device')

# 2. Update stats labels
content = content.replace('Total Laptops', 'Total Devices')

# 3. Update success message to be dynamic
old_msg = "document.getElementById('msg').textContent = '✅ Laptop added successfully!';"
new_msg = """const deviceType = document.getElementById('deviceType').value;
        const msgText = deviceType === 'Phone' ? '✅ Phone added successfully!' : '✅ Laptop added successfully!';
        document.getElementById('msg').textContent = msgText;"""
content = content.replace(old_msg, new_msg)

with open('public/dashboard.html', 'w') as f:
    f.write(content)

print("✅ All labels updated to 'Device'! Messages will now be dynamic.")
