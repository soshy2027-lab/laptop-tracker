with open('public/terms.html', 'r') as f:
    html = f.read()

old_text = "support@laptoptracker.com"
new_text = '<a href="/contact.html" style="color: #667eea; text-decoration: none; font-weight: bold;">support@laptoptracker.com</a>'

if old_text in html:
    html = html.replace(old_text, new_text)
    with open('public/terms.html', 'w') as f:
        f.write(html)
    print("Terms page link updated!")
else:
    print("Text not found!")
