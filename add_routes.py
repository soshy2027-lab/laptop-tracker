with open('server.js', 'r') as f:
    content = f.read()

new_routes = """
// Profile and Settings Routes
app.get('/profile', (req, res) => {
  res.sendFile(__dirname + '/public/profile.html');
});

app.get('/settings', (req, res) => {
  res.sendFile(__dirname + '/public/settings.html');
});
"""

if 'app.listen' in content:
    content = content.replace('app.listen', new_routes + '\napp.listen')
    with open('server.js', 'w') as f:
        f.write(content)
    print("Routes added successfully!")
else:
    print("Could not find app.listen. Please check server.js")
