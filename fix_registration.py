with open('public/index.html', 'r') as f:
    html = f.read()

# Find the register form and replace it with professional version
old_form = '''<div id="register-form" class="form" style="display: none;">
    <input type="text" id="register-name" placeholder="Full Name" required>
    <input type="email" id="register-email" placeholder="Email" required>
    <input type="password" id="register-password" placeholder="Password" required>
    <button class="btn-primary" onclick="handleRegister()">Create Account</button>
    <p id="register-error" style="color: red; margin-top: 10px;"></p>
  </div>'''

new_form = '''<div id="register-form" class="form" style="display: none;">
    <div class="form-row">
      <input type="text" id="register-firstname" placeholder="First Name" required style="flex: 1;">
      <input type="text" id="register-lastname" placeholder="Last Name" required style="flex: 1;">
    </div>
    <input type="text" id="register-fullname" placeholder="Full Name" required>
    <input type="text" id="register-nationality" placeholder="Nationality" required>
    <input type="tel" id="register-phone" placeholder="Phone Number (e.g., +254...)" required>
    <input type="email" id="register-email" placeholder="Email" required>
    <input type="password" id="register-password" placeholder="Password" required>
    
    <div style="margin: 15px 0; padding: 15px; background: #f9fafb; border-radius: 8px; text-align: left;">
      <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Profile Photo</label>
      <input type="file" id="register-photo" accept="image/jpeg,image/png" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 5px;">
      <small style="color: #666; font-size: 12px;">Upload JPG or PNG (Max 2MB)</small>
    </div>
    
    <button class="btn-primary" onclick="handleRegister()">Create Account</button>
    <p id="register-error" style="color: red; margin-top: 10px;"></p>
  </div>'''

# Add CSS for the form row
css_addition = '''<style>
  .form-row { display: flex; gap: 10px; margin-bottom: 10px; }
  .form-row input { flex: 1; }
</style>'''

html = html.replace(old_form, new_form)
if '</head>' in html:
    html = html.replace('</head>', css_addition + '\n</head>')

with open('public/index.html', 'w') as f:
    f.write(html)
print("Registration form updated!")
