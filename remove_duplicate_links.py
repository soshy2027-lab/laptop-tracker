import re

with open('public/index.html', 'r') as f:
    html = f.read()

# Pattern to match the first set of links inside the container
pattern = r'\s*<div style="display: flex; justify-content: center; gap: 15px; margin-top: 10px;">\s*<a href="/important\.html"[^>]*>Important</a>\s*<a href="/terms\.html"[^>]*>Terms</a>\s*<a href="/about\.html"[^>]*>About</a>\s*</div>'

html = re.sub(pattern, '', html)

with open('public/index.html', 'w') as f:
    f.write(html)
print("Duplicate links removed!")
