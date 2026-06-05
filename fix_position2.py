with open('public/index.html', 'r') as f:
    html = f.read()

# Replace the entire auth-extras style and structure
old_extras = """#auth-extras { max-width: 400px; margin: 10px auto; padding: 10px; text-align: center; }
  #show-forgot-btn { display: block; margin: 15px auto 0; text-align: center; }"""

new_extras = """#auth-extras { max-width: 400px; margin: 0 auto; padding: 0; text-align: center; }
  #show-forgot-btn { display: block; margin: 15px auto 0; text-align: center; font-size: 14px; }
  .auth-form { display: none; margin: 15px auto 0; padding: 20px; background: #f9fafb; border-radius: 8px; text-align: left; max-width: 400px; }"""

html = html.replace(old_extras, new_extras)

with open('public/index.html', 'w') as f:
    f.write(html)
print("Positioning fixed v2!")
