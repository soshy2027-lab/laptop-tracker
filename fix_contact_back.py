with open('public/contact.html', 'r') as f:
    html = f.read()

# Change "Back to Login" to "Back" and make it go back to previous page
old_back = '''<div class="back-link">
      <a href="/">← Back to Login</a>
    </div>'''

new_back = '''<div class="back-link">
      <a href="javascript:history.back()">← Go Back</a>
    </div>'''

if old_back in html:
    html = html.replace(old_back, new_back)
    with open('public/contact.html', 'w') as f:
        f.write(html)
    print("Back button fixed!")
else:
    print("Back button not found!")
