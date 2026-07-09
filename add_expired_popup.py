with open('public/dashboard.html', 'r') as f:
    html = f.read()

# 1. Change the instant redirect to show a popup instead
old_check = "if(data.status === 'expired') window.location.href = '/subscription';"
new_check = "if(data.status === 'expired') showExpiredPopup();"
html = html.replace(old_check, new_check)

# 2. Add the popup HTML and script right before the closing body tag
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
html = html.replace('</body>', popup_code + '</body>')

with open('public/dashboard.html', 'w') as f:
    f.write(html)

print("✅ Expired popup added safely!")
