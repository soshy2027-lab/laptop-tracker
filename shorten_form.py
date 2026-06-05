import re

with open('public/index.html', 'r') as f:
    html = f.read()

# 1. Remove the Nationality field
html = re.sub(r'\s*<input type="text" id="register-nationality"[^>]*>', '', html)

# 2. Remove the Profile Photo block safely
html = re.sub(r'\s*<div style="margin-bottom: 10px; padding: 10px; background: #f9fafb; border-radius: 5px;">.*?Profile Photo.*?</div>', '', html, flags=re.DOTALL)

with open('public/index.html', 'w') as f:
    f.write(html)
print("Form shortened successfully!")
