import re

with open('public/index.html', 'r') as f:
    html = f.read()

# 1. Remove the First Name / Last Name row
html = re.sub(r'\s*<div style="display: flex; gap: 10px; margin-bottom: 10px;">.*?</div>', '', html, flags=re.DOTALL)

# 2. Remove the extra Full Name field we added
html = re.sub(r'\s*<input type="text" id="register-fullname"[^>]*>', '', html)

# 3. Update the phone label to "Contact"
html = html.replace('placeholder="Phone Number (e.g., +254...)"', 'placeholder="Contact (e.g., +254...)"')

with open('public/index.html', 'w') as f:
    f.write(html)
print("Form cleaned up!")
