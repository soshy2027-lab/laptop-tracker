with open('public/dashboard.html', 'r') as f:
    content = f.read()

# Find the old "white box" code
old_cell = """<td><span style="background:${l.deviceType === 'Phone' ? '#fef3c7' : '#dbeafe'}; color:${l.deviceType === 'Phone' ? '#92400e' : '#1e40af'}; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:bold;">${l.deviceType === 'Phone' ? '📱 Phone' : ' Laptop'}</span></td>"""

# Replace it with clean, simple text that fits your dark theme perfectly
new_cell = """<td style="font-weight:bold; color:#e5e7eb;">${l.deviceType === 'Phone' ? ' Phone' : '💻 Laptop'}</td>"""

if old_cell in content:
    content = content.replace(old_cell, new_cell)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Table cleaned up! The white box is gone.")
else:
    print("❌ Could not find the exact cell code.")
