with open('public/index.html', 'r') as f:
    html = f.read()

new_fields = """
    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
      <input type="text" id="register-firstname" placeholder="First Name" required style="flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 5px;">
      <input type="text" id="register-lastname" placeholder="Last Name" required style="flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 5px;">
    </div>
    <input type="text" id="register-fullname" placeholder="Full Name" required style="width: 100%; padding: 12px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;">
    <input type="text" id="register-nationality" placeholder="Nationality" required style="width: 100%; padding: 12px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;">
    <input type="tel" id="register-phone" placeholder="Phone Number (e.g., +254...)" required style="width: 100%; padding: 12px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;">
    <div style="margin-bottom: 10px; padding: 10px; background: #f9fafb; border-radius: 5px;">
      <label style="font-size: 14px; color: #333; display: block; margin-bottom: 5px;">Profile Photo</label>
      <input type="file" id="register-photo" accept="image/jpeg,image/png" style="width: 100%;">
    </div>
"""

target = "<!-- PASSWORD STRENGTH METER -->"
if target in html:
    html = html.replace(target, new_fields + "    " + target)
    with open('public/index.html', 'w') as f:
        f.write(html)
    print("Fields added successfully!")
else:
    print("Target not found!")
