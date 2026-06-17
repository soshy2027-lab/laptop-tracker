with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Update the empty table message to match the new column count
content = content.replace('colspan="9"', 'colspan="10"')

# 2. Add the Type cell to the row, right before the Brand cell
old_row = """          <tr>
            <td><strong>${l.brand||''}</strong></td>"""

new_row = """          <tr>
            <td>${l.deviceType === 'Phone' ? '📱 Phone' : '💻 Laptop'}</td>
            <td><strong>${l.brand||''}</strong></td>"""

if old_row in content:
    content = content.replace(old_row, new_row, 1)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Table rows updated safely! Type column is now live.")
else:
    print("❌ Could not find the row code. Let me know!")
