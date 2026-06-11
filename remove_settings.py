import os

# 1. Remove Settings button from dashboard menu
with open('public/dashboard.html', 'r') as f:
    html = f.read()
html = html.replace('  <button onclick="window.location.href=\'/settings\'">Settings</button>\n', '')
with open('public/dashboard.html', 'w') as f:
    f.write(html)
print("Settings button removed from menu!")

# 2. Delete the settings.html file
if os.path.exists('public/settings.html'):
    os.remove('public/settings.html')
    print("settings.html file deleted!")

# 3. Remove Settings route from server.js
with open('server.js', 'r') as f:
    content = f.read()

old_block = """
// Profile and Settings Routes
app.get('/profile', (req, res) => {
  res.sendFile(__dirname + '/public/profile.html');
});

app.get('/settings', (req, res) => {
  res.sendFile(__dirname + '/public/settings.html');
});
"""

new_block = """
// Profile Route
app.get('/profile', (req, res) => {
  res.sendFile(__dirname + '/public/profile.html');
});
"""

content = content.replace(old_block, new_block)
with open('server.js', 'w') as f:
    f.write(content)
print("Settings route removed from server!")
