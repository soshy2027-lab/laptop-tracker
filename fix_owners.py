# 1. Fix server.js to link user names to laptops
with open('server.js', 'r') as f:
    server = f.read()

old_laptop_route = "const laptops = await Laptop.find();"
new_laptop_route = "const laptops = await Laptop.find().populate('user', 'name');"

# Replace the first occurrence (which is in the laptops route)
server = server.replace(old_laptop_route, new_laptop_route, 1)

with open('server.js', 'w') as f:
    f.write(server)

# 2. Fix admin.html to display the linked name
with open('public/admin.html', 'r') as f:
    html = f.read()

old_display = "html += `<tr><td>${l.ownerName || 'Unknown'}</td><td>${l.brand} ${l.model}</td><td>${l.serialNumber}</td><td>${l.stolen ? '🚨 STOLEN' : ' ✅ Active'}</td></tr>`;"
new_display = "html += `<tr><td>${l.user?.name || 'Unknown'}</td><td>${l.brand || ''} ${l.model || ''}</td><td>${l.serialNumber || l.serial || 'Unknown'}</td><td>${l.stolen ? '🚨 STOLEN' : ' ✅ Active'}</td></tr>`;"

html = html.replace(old_display, new_display)

with open('public/admin.html', 'w') as f:
    f.write(html)

print("✅ Owners fixed!")
