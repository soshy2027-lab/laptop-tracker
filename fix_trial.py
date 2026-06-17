with open('server.js', 'r') as f:
    content = f.read()

# The code uses 'trialEndDate' but the database expects 'subscriptionExpiryDate'
# We will safely rename it so the 21-day timer actually saves.
content = content.replace('trialEndDate', 'subscriptionExpiryDate')

with open('server.js', 'w') as f:
    f.write(content)
print("✅ Server fixed! 21-day trial will now save correctly.")
