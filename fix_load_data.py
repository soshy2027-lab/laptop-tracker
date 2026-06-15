with open('public/dashboard.html', 'r') as f:
    content = f.read()

# Find the initial loadData() call at the bottom of the script and wrap it in DOMContentLoaded
old_line = "    loadData();"
new_line = "    document.addEventListener('DOMContentLoaded', loadData);"

# We only want to replace the LAST occurrence (the initial call at the bottom)
last_idx = content.rfind(old_line)

if last_idx != -1:
    content = content[:last_idx] + new_line + content[last_idx + len(old_line):]
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("Fixed data loading timing!")
else:
    print("Could not find the line to fix!")
