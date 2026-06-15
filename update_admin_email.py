with open('server.js', 'r') as f:
    content = f.read()

old_email = """await resend.emails.send({ from: process.env.FROM_EMAIL || 'onboarding@resend.dev', to: ADMIN_EMAIL, subject: 'STOLEN LAPTOP ALERT', html: '<h2>Stolen Laptop Reported</h2><p>User: ' + req.user.email + '</p><p>Laptop: ' + (laptop.brand || '') + ' ' + (laptop.model || '') + ' | Serial: ' + laptop.serial + '</p><p>Location: ' + location + '</p><p><a href="' + mapUrl + '">View on Map</a></p>' });"""

new_email = """await resend.emails.send({ from: process.env.FROM_EMAIL || 'onboarding@resend.dev', to: ADMIN_EMAIL, subject: 'STOLEN LAPTOP ALERT', html: '<h2>Stolen Laptop Reported</h2><p>User: ' + req.user.email + '</p><p>Laptop: ' + (laptop.brand || '') + ' ' + (laptop.model || '') + ' | Serial: ' + laptop.serial + '</p><p><strong>OB Number:</strong> ' + (laptop.obNumber || 'Not provided') + '</p><p><strong>Police Station:</strong> ' + (laptop.policeStation || 'Not provided') + '</p><p><strong>Report Date:</strong> ' + (laptop.reportDate ? new Date(laptop.reportDate).toLocaleDateString() : 'Not provided') + '</p><p>Location: ' + location + '</p><p><a href="' + mapUrl + '">View on Map</a></p>' });"""

if old_email in content:
    content = content.replace(old_email, new_email)
    with open('server.js', 'w') as f:
        f.write(content)
    print("Admin email updated successfully!")
else:
    print("Could not find admin email to replace!")
