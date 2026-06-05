with open('public/dashboard.html', 'r') as f:
    html = f.read()

# Fix the menu buttons to call the correct original functions
old_buttons = """<button onclick="document.getElementById('watch-btn') ? document.getElementById('watch-btn').click() : alert('Watch feature')">Watch</button>
  <button onclick="window.location.href='/subscription'">Subscribe</button>
  <button onclick="toggleMode()">Mode</button>
  <button onclick="handleLogout()">Logout</button>"""

new_buttons = """<button onclick="openVideo()">Watch</button>
  <button onclick="window.location.href='/subscription'">Subscribe</button>
  <button onclick="toggleTheme()">Mode</button>
  <button onclick="logout()">Logout</button>"""

html = html.replace(old_buttons, new_buttons)

with open('public/dashboard.html', 'w') as f:
    f.write(html)
print("Menu functions fixed!")
