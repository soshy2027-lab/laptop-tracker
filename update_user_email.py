with open('server.js', 'r') as f:
    content = f.read()

old_email = """await resend.emails.send({ from: process.env.FROM_EMAIL || 'onboarding@resend.dev', to: req.user.email, subject: 'Your Laptop Marked as Stolen', html: '<h2>Laptop Marked as Stolen</h2><p>Your laptop ' + (laptop.brand || '') + ' ' + (laptop.model || '') + ' (Serial: ' + laptop.serial + ') has been marked as stolen.</p><p>Location: ' + location + '</p><p><a href="' + mapUrl + '">View Location</a></p>' });"""

new_email = """await resend.emails.send({ from: process.env.FROM_EMAIL || 'onboarding@resend.dev', to: req.user.email, subject: 'Your Laptop Marked as Stolen', html: '<h2>Laptop Marked as Stolen</h2><p>Your laptop ' + (laptop.brand || '') + ' ' + (laptop.model || '') + ' (Serial: ' + laptop.serial + ') has been marked as stolen.</p><p><strong>OB Number:</strong> ' + (laptop.obNumber || 'Not provided') + '</p><p><strong>Police Station:</strong> ' + (laptop.policeStation || 'Not provided') + '</p><p><strong>Report Date:</strong> ' + (laptop.reportDate ? new Date(laptop.reportDate).toLocaleDateString() : 'Not provided') + '</p><p>Location: ' + location + '</p><p><a href="' + mapUrl + '">View Location</a></p>' });"""

if old_email in content:
    content = content.replace(old_email, new_email)
    with open('server.js', 'w') as f:
        f.write(content)
    print("User email updated successfully!")
else:
    print("Could not find user email to replace!")
