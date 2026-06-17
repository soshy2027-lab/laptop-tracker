with open('public/dashboard.html', 'r') as f:
    content = f.read()

# Fix the ID mismatch so the button works
old_find = "const l = laptops.find(x => x._id === id);"
new_find = "const l = laptops.find(x => String(x._id) === id);"

if old_find in content:
    content = content.replace(old_find, new_find, 1)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Police Report button logic fixed!")
else:
    print("❌ Could not find the find function.")
