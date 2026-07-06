with open('public/dashboard.html', 'r') as f:
    html = f.read()

# Find and replace the toggleStolen function to add subscription check
old_toggle = """window.toggleStolen = (id, stolen) => {
      if (!stolen) {
        if (!confirm('✅ Mark this laptop as safe?')) return;
        sendStolenUpdate(id, false);
      } else {
        pendingStolenId = id;
        document.getElementById('obDate').value = new Date().toISOString().split('T')[0];
        document.getElementById('obModal').style.display = 'block';
      }
    };"""

new_toggle = """window.toggleStolen = async (id, stolen) => {
      if (!stolen) {
        if (!confirm('✅ Mark this laptop as safe?')) return;
        sendStolenUpdate(id, false);
      } else {
        // CHECK SUBSCRIPTION BEFORE ALLOWING STOLEN REPORT
        try {
          const res = await fetch('/api/subscription/status', { headers: auth });
          const data = await res.json();
          
          if (data.status === 'expired') {
            alert('🚨 SUBSCRIPTION REQUIRED\\n\\nTo protect your device and use the stolen tracking feature, you must have an active subscription.\\n\\nYour free trial has ended. Please subscribe now to continue using Laptop Tracker services.');
            window.location.href = '/subscription';
            return;
          }
          
          // Subscription active - allow stolen reporting
          pendingStolenId = id;
          document.getElementById('obDate').value = new Date().toISOString().split('T')[0];
          document.getElementById('obModal').style.display = 'block';
        } catch (err) {
          alert('Error checking subscription. Please try again.');
        }
      }
    };"""

html = html.replace(old_toggle, new_toggle)

with open('public/dashboard.html', 'w') as f:
    f.write(html)

print("✅ Stolen feature blocked for expired users!")
