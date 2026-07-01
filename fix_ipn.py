with open('server.js', 'r') as f:
    server = f.read()

# Remove the notification_id field or set it properly
old_order = """notification_id: '',"""
new_order = """notification_id: null,"""

server = server.replace(old_order, new_order)

with open('server.js', 'w') as f:
    f.write(server)

print("✅ IPN notification_id fixed!")
