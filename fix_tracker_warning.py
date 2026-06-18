with open('public/tracker.html', 'r') as f:
    content = f.read()

old_html = '<h1>Laptop Tracker</h1>'
new_html = """<h1>Laptop Tracker</h1>
      <div style="background: #fff3cd; color: #856404; padding: 15px; border-radius: 8px; border: 1px solid #ffeeba; margin-bottom: 20px; font-size: 0.9rem; text-align: left;">
        <strong>⚠️ Important:</strong> Only open this page on the device you want to protect. Do not open this on a different phone!
      </div>"""

if old_html in content:
    content = content.replace(old_html, new_html)
    with open('public/tracker.html', 'w') as f:
        f.write(content)
    print("✅ Warning added to tracker page safely!")
else:
    print("❌ Could not find the exact code.")
