with open('public/dashboard.html', 'r') as f:
    html = f.read()

# 1. Fix the color to always be Green when not stolen
old_color = "const statusColor = l.stolen ? '#ef4444' : l.status==='Active' ? '#10b981' : '#f59e0b';"
new_color = "const statusColor = l.stolen ? '#ef4444' : '#10b981';"

# 2. Fix the text to always say Active when not stolen
old_text = "const statusText = l.stolen ? '🚨 STOLEN' : (l.status || 'Active');"
new_text = "const statusText = l.stolen ? '🚨 STOLEN' : '✅ Active';"

html = html.replace(old_color, new_color)
html = html.replace(old_text, new_text)

with open('public/dashboard.html', 'w') as f:
    f.write(html)
print("Active status fixed!")
