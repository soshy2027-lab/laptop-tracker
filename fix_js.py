with open('public/dashboard.html', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'const data = {' in line:
        indent = line[:len(line) - len(line.lstrip())]
        lines.insert(i + 1, indent + "  deviceType: document.getElementById('deviceType').value,\n")
        break

with open('public/dashboard.html', 'w') as f:
    f.writelines(lines)
print("✅ JavaScript updated safely! The form will now send the device type.")
