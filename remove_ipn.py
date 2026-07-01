with open('server.js', 'r') as f:
    server = f.read()

# Completely remove the notification_id line
import re
server = re.sub(r"\s*notification_id:\s*null,?\n", "", server)
server = re.sub(r"\s*notification_id:\s*'',?\n", "", server)

with open('server.js', 'w') as f:
    f.write(server)

print("✅ notification_id field removed!")
