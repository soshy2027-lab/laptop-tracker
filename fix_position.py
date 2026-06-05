with open('public/index.html', 'r') as f:
    html = f.read()

# Replace the old style with better positioning
old_style = """.auth-form { display: none; margin-top: 20px; padding: 15px; background: #f9fafb; border-radius: 8px; text-align: left; }"""

new_style = """.auth-form { display: none; margin-top: 20px; padding: 15px; background: #f9fafb; border-radius: 8px; text-align: left; }
  #auth-extras { max-width: 400px; margin: 10px auto; padding: 10px; text-align: center; }
  #show-forgot-btn { display: block; margin: 15px auto 0; text-align: center; }"""

html = html.replace(old_style, new_style)

with open('public/index.html', 'w') as f:
    f.write(html)
print("Positioning fixed!")
