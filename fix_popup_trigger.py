with open('public/dashboard.html', 'r') as f:
    html = f.read()

# Change the trigger to check if they are NOT subscribed
old_trigger = "if(data.status === 'expired') showExpiredPopup();"
new_trigger = "if(data.status === 'expired' || data.isSubscribed === false) showExpiredPopup();"

if old_trigger in html:
    html = html.replace(old_trigger, new_trigger)
    with open('public/dashboard.html', 'w') as f:
        f.write(html)
    print("✅ Popup trigger updated!")
else:
    print("⚠️ Trigger not found exactly as expected. Checking alternative...")
    # Fallback if the code was slightly different
    import re
    html = re.sub(r"if\s*\(\s*data\.status\s*===\s*['\"]expired['\"]\s*\)\s*showExpiredPopup\(\);", new_trigger, html)
    with open('public/dashboard.html', 'w') as f:
        f.write(html)
    print("✅ Popup trigger updated (fallback)!")
