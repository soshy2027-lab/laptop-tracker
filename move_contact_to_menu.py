# First, remove Contact Us from login page footer
with open('public/index.html', 'r') as f:
    html = f.read()

old_links = '''<a href="/important.html" style="color: #666; text-decoration: none; font-size: 12px;">Important</a>
        <a href="/terms.html" style="color: #666; text-decoration: none; font-size: 12px;">Terms</a>
        <a href="/about.html" style="color: #666; text-decoration: none; font-size: 12px;">About</a>
        <a href="/contact.html" style="color: #666; text-decoration: none; font-size: 12px;">Contact Us</a>'''

new_links = '''<a href="/important.html" style="color: #666; text-decoration: none; font-size: 12px;">Important</a>
        <a href="/terms.html" style="color: #666; text-decoration: none; font-size: 12px;">Terms</a>
        <a href="/about.html" style="color: #666; text-decoration: none; font-size: 12px;">About</a>'''

if old_links in html:
    html = html.replace(old_links, new_links)
    with open('public/index.html', 'w') as f:
        f.write(html)
    print("Contact link removed from login page!")
else:
    print("Login page links not found!")

# Second, add Contact Us to dashboard menu before Logout
with open('public/dashboard.html', 'r') as f:
    html = f.read()

old_menu = '''<button onclick="openVideo()">Watch</button>
  <button onclick="window.location.href='/subscription'">Subscribe</button>
  <button onclick="toggleTheme()">Mode</button>
  <button onclick="logout()">Logout</button>'''

new_menu = '''<button onclick="openVideo()">Watch</button>
  <button onclick="window.location.href='/subscription'">Subscribe</button>
  <button onclick="toggleTheme()">Mode</button>
  <button onclick="window.location.href='/contact.html'">Contact Us</button>
  <button onclick="logout()">Logout</button>'''

if old_menu in html:
    html = html.replace(old_menu, new_menu)
    with open('public/dashboard.html', 'w') as f:
        f.write(html)
    print("Contact Us added to dashboard menu!")
else:
    print("Dashboard menu not found!")
