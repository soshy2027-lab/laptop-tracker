with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Change titles safely
content = content.replace('<h2>Add New Laptop</h2>', '<h2>Add New Device</h2>')
content = content.replace('<h2>My Laptops</h2>', '<h2>My Devices</h2>')

# 2. Change button text safely
content = content.replace('<button type="submit" class="btn-add">Add Laptop</button>', '<button type="submit" class="btn-add">Add Device</button>')

# 3. Change search placeholder safely
content = content.replace('placeholder=" Search laptops..."', 'placeholder="🔍 Search devices..."')

# 4. Add the dropdown menu safely right after the form tag
old_form = '<form id="addForm">'
new_form = '''<form id="addForm">
    <label style="font-weight:bold; display:block; margin-bottom:5px;">Select Device Type:</label>
    <select id="deviceType" style="width:100%; padding:10px; margin-bottom:15px; border:1px solid #ccc; border-radius:5px; font-size:16px;">
        <option value="Laptop"> Laptop</option>
        <option value="Phone">📱 Phone</option>
    </select>'''

if old_form in content:
    content = content.replace(old_form, new_form)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Form updated safely! No existing code was rewritten.")
else:
    print("❌ Could not find form.")
