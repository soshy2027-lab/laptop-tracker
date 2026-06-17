with open('public/dashboard.html', 'r') as f:
    content = f.read()

# Add the "Type" header right before "Brand"
old_header = "              <th>Brand</th>"
new_header = "              <th>Type</th>\n              <th>Brand</th>"

if old_header in content:
    content = content.replace(old_header, new_header, 1)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Added 'Type' column header safely!")
else:
    print("❌ Could not find the Brand header.")
