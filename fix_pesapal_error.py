with open('server.js', 'r') as f:
    server = f.read()

# Replace the vague error with detailed error
old_error = 'res.status(500).json({ error: \'Pesapal failed\' });'
new_error = '''res.status(500).json({ 
      error: 'Pesapal failed', 
      details: err.response?.data || err.message,
      status: err.response?.status 
    });'''

server = server.replace(old_error, new_error)

with open('server.js', 'w') as f:
    f.write(server)

print("✅ Error logging fixed - now shows real error!")
