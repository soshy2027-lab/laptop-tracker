with open('public/index.html', 'r') as f:
    html = f.read()

# Find the footer links and add Contact Us
old_links = '''<a href="/important.html" style="color: #666; text-decoration: none; font-size: 12px;">Important</a>
        <a href="/terms.html" style="color: #666; text-decoration: none; font-size: 12px;">Terms</a>
        <a href="/about.html" style="color: #666; text-decoration: none; font-size: 12px;">About</a>'''

new_links = '''<a href="/important.html" style="color: #666; text-decoration: none; font-size: 12px;">Important</a>
        <a href="/terms.html" style="color: #666; text-decoration: none; font-size: 12px;">Terms</a>
        <a href="/about.html" style="color: #666; text-decoration: none; font-size: 12px;">About</a>
        <a href="/contact.html" style="color: #666; text-decoration: none; font-size: 12px;">Contact Us</a>'''

if old_links in html:
    html = html.replace(old_links, new_links)
    with open('public/index.html', 'w') as f:
        f.write(html)
    print("Contact link added!")
else:
    print("Links not found!")
