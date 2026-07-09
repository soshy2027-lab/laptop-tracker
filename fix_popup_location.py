import re

with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Remove the incorrectly placed popup code using regex
pattern = r'<div id="expiredPopup".*?</script>'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# 2. Define the correct popup code
popup_code = """
<div id="expiredPopup" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; justify-content:center; align-items:center;">
  <div style="background:white; padding:30px; border-radius:15px; text-align:center; max-width:90%; width:400px; box-shadow:0 10px 25px rgba(0,0,0,0.5);">
    <h2 style="color:#dc2626; margin-top:0;">⚠️ Trial Expired</h2>
    <p style="font-size:16px; color:#333; margin-bottom:20px;">Your 21-day free trial has ended. Please subscribe to continue protecting your devices and accessing all Laptop Tracker features.</p>
    <button onclick="window.location.href='/subscription'" style="background:#2563eb; color:white; border:none; padding:12px 24px; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; width:100%;">Subscribe Now</button>
    <button onclick="document.getElementById('expiredPopup').style.display='none'" style="background:#e5e7eb; color:#333; border:none; padding:10px 24px; border-radius:8px; font-size:14px; margin-top:10px; cursor:pointer; width:100%;">Maybe Later</button>
  </div>
</div>
<script>
  function showExpiredPopup() {
    document.getElementById('expiredPopup').style.display = 'flex';
  }
</script>
"""

# 3. Insert it right before the LAST </body> tag (the real end of the file)
last_body_index = content.rfind('</body>')
if last_body_index != -1:
    content = content[:last_body_index] + popup_code + '\n' + content[last_body_index:]

with open('public/dashboard.html', 'w') as f:
    f.write(content)

print("✅ Fixed popup location safely!")
