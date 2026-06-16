with open('public/index.html', 'r') as f:
    content = f.read()

old_block = """        <div id="strength-text" class="strength-text"></div>
      </div>
      <button class="btn-primary" onclick="handleRegister()">Create Account</button>
    </div>"""

new_block = """        <div id="strength-text" class="strength-text"></div>
      </div>
      
      <div style="background: #f0fdf4; border: 2px dashed #16a34a; padding: 15px; border-radius: 8px; margin: 20px 0 15px 0; text-align: center;">
        <p style="margin: 0; font-weight: bold; color: #15803d; font-size: 18px;">🎉 21 Days FREE Trial! 🎉</p>
        <p style="margin: 5px 0 0 0; font-size: 14px; color: #4b5563;">Sign up now. No credit card required. Full access!</p>
      </div>
      
      <button class="btn-primary" onclick="handleRegister()">Create Account</button>
    </div>"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('public/index.html', 'w') as f:
        f.write(content)
    print("✅ 21 Days Free Trial box added successfully!")
else:
    print("❌ Could not find the exact button block. Let me know!")
