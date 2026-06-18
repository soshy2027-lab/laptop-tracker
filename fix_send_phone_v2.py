with open('public/dashboard.html', 'r') as f:
    lines = f.readlines()

# Find the exact line where the form sends the brand
for i, line in enumerate(lines):
    if "brand: document.getElementById('brand').value," in line:
        # Make sure we are in the form submit section (around line 524)
        if i > 500 and i < 550:
            indent = line[:len(line) - len(line.lstrip())]
            # Insert deviceType right before brand with the exact same spacing
            lines.insert(i, f"{indent}deviceType: document.getElementById('deviceType').value,\n")
            break

with open('public/dashboard.html', 'w') as f:
    f.writelines(lines)
print("✅ Fixed! The form will now send 'Phone' to the database.")
