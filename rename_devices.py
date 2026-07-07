with open('public/admin.html', 'r') as f:
    html = f.read()

# 1. Rename the tab from Laptops to Devices
html = html.replace("onclick=\"switchTab('laptops')\">💻 Laptops", "onclick=\"switchTab('laptops')\">📱 Devices")

# 2. Add "Type" to the table header
html = html.replace("<th>Owner</th><th>Brand/Model</th><th>Serial</th><th>Status</th>", "<th>Type</th><th>Owner</th><th>Brand/Model</th><th>Serial</th><th>Status</th>")

# 3. Add the device type (Phone or Laptop) to the table rows
old_row = "html += `<tr><td>${l.ownerName || 'Unknown'}</td><td>${l.brand || ''} ${l.model || ''}</td><td>${l.serialNumber || l.serial || 'Unknown'}</td><td>${l.stolen ? '🚨 STOLEN' : ' ✅ Active'}</td></tr>`;"
new_row = "html += `<tr><td>${l.deviceType === 'Phone' ? '📱 Phone' : '💻 Laptop'}</td><td>${l.ownerName || 'Unknown'}</td><td>${l.brand || ''} ${l.model || ''}</td><td>${l.serialNumber || l.serial || 'Unknown'}</td><td>${l.stolen ? '🚨 STOLEN' : ' ✅ Active'}</td></tr>`;"
html = html.replace(old_row, new_row)

with open('public/admin.html', 'w') as f:
    f.write(html)

print("✅ Admin tab updated to show Phones and Laptops!")
