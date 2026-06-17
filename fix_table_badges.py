with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Fix the table cell to show a clean, professional badge
old_cell = "<td>${l.deviceType === 'Phone' ? '📱 Phone' : ' Laptop'}</td>"
new_cell = """<td><span style="background:${l.deviceType === 'Phone' ? '#fef3c7' : '#dbeafe'}; color:${l.deviceType === 'Phone' ? '#92400e' : '#1e40af'}; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:bold;">${l.deviceType === 'Phone' ? '📱 Phone' : '💻 Laptop'}</span></td>"""

if old_cell in content:
    content = content.replace(old_cell, new_cell)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Table updated with professional badges!")
else:
    print("❌ Could not find the exact cell code. Let me know!")
