with open('public/dashboard.html', 'r') as f:
    html = f.read()

# Find the menu section
old_menu = '''<button onclick="openVideo()">Watch</button>
  <button onclick="window.location.href='/subscription'">Subscribe</button>
  <button onclick="toggleTheme()">Mode</button>
  <button onclick="window.location.href='/contact.html'">Contact Us</button>
  <button onclick="logout()">Logout</button>'''

new_menu = '''<button onclick="openVideo()">Watch</button>
  <button onclick="window.location.href='/subscription'">Subscribe</button>
  <button onclick="toggleTheme()">Mode</button>
  <button onclick="window.location.href='/contact.html'">Contact Us</button>
  <button onclick="window.location.href='/profile'">Profile</button>
  <button onclick="window.location.href='/dashboard'">Homepage</button>
  <button onclick="window.location.href='/settings'">Settings</button>
  <button onclick="logout()">Logout</button>'''

if old_menu in html:
    html = html.replace(old_menu, new_menu)
    with open('public/dashboard.html', 'w') as f:
        f.write(html)
    print("Menu items added!")
else:
    print("Menu not found!")
