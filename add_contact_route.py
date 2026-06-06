with open('server.js', 'r') as f:
    code = f.read()

new_route = """
// Contact Form Route
app.post('/api/contact', async (req, res) => {
  const { name, email, subject, message } = req.body;
  if (!name || !email || !subject || !message) {
    return res.status(400).json({ error: 'All fields are required' });
  }
  try {
    await resend.emails.send({
      from: process.env.FROM_EMAIL || 'onboarding@resend.dev',
      to: ADMIN_EMAIL || 'support@laptoptracker.com',
      subject: 'Contact Form: ' + subject + ' (from ' + name + ')',
      html: '<h2>New Contact Form Submission</h2><p><strong>Name:</strong> ' + name + '</p><p><strong>Email:</strong> ' + email + '</p><p><strong>Subject:</strong> ' + subject + '</p><p><strong>Message:</strong><br>' + message.replace(/\\n/g, '<br>') + '</p>'
    });
    res.json({ message: 'Email sent successfully' });
  } catch (err) {
    console.error('Contact email error:', err);
    res.status(500).json({ error: 'Failed to send email' });
  }
});

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));"""

target = "app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));"

if target in code:
    code = code.replace(target, new_route)
    with open('server.js', 'w') as f:
        f.write(code)
    print("Contact route added!")
else:
    print("Target not found!")
