with open('public/index.html', 'r') as f:
    html = f.read()

# Fix the container to force it below the login form
old_container = """#auth-extras { max-width: 400px; margin: 20px auto; padding: 10px; text-align: center; }"""
new_container = """#auth-extras { width: 100%; max-width: 400px; margin: 20px auto 0; padding: 10px; text-align: center; clear: both; display: block; }"""

# Fix the form to remove the boxy background
old_form = """.auth-form { display: none; margin-top: 20px; padding: 15px; background: #f9fafb; border-radius: 8px; text-align: left; }"""
new_form = """.auth-form { display: none; margin-top: 10px; padding: 0; background: transparent; text-align: center; }"""

html = html.replace(old_container, new_container)
html = html.replace(old_form, new_form)

with open('public/index.html', 'w') as f:
    f.write(html)
print("CSS fixed!")
