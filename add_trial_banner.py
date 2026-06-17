with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Add the Banner HTML right above the stats
banner_html = """    <!-- FREE TRIAL BANNER -->
    <div id="trialBanner" class="trial-banner" style="display:none;">
      <div class="trial-content">
        <span class="trial-icon">⏳</span>
        <div class="trial-text">
          <strong>Free Trial Active</strong>
          <span id="trialDays">Loading...</span>
        </div>
        <a href="/subscription" class="trial-btn">Subscribe Now</a>
      </div>
    </div>

"""
content = content.replace('    <div class="stats">', banner_html + '    <div class="stats">')

# 2. Add the CSS for the banner
css_code = """
    /* Trial Banner Styling */
    .trial-banner { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .trial-content { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
    .trial-icon { font-size: 24px; }
    .trial-text { display: flex; flex-direction: column; }
    .trial-text strong { font-size: 16px; }
    .trial-text span { font-size: 14px; opacity: 0.9; }
    .trial-btn { background: white; color: #d97706; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; }
"""
content = content.replace('</style>', css_code + '\n  </style>')

# 3. Add the JavaScript to calculate and show the days
js_code = """
    // Free Trial Countdown Logic
    async function loadTrialInfo() {
      try {
        const res = await fetch('/api/profile', { headers: auth });
        if (res.ok) {
          const data = await res.json();
          if (data.subscriptionExpiryDate && !data.isSubscribed) {
            const expiry = new Date(data.subscriptionExpiryDate);
            const now = new Date();
            const diffDays = Math.ceil((expiry - now) / (1000 * 60 * 60 * 24));
            if (diffDays > 0) {
              document.getElementById('trialDays').textContent = diffDays + ' days remaining';
              document.getElementById('trialBanner').style.display = 'block';
            }
          }
        }
      } catch(e) {}
    }
    loadTrialInfo();
"""
content = content.replace('</script>', js_code + '\n  </script>')

with open('public/dashboard.html', 'w') as f:
    f.write(content)

print("✅ Beautiful trial countdown banner added safely!")
