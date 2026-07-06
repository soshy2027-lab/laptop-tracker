with open('public/dashboard.html', 'r') as f:
    html = f.read()

# Replace the trial banner with a more urgent one
old_banner = """<!-- FREE TRIAL BANNER -->
    <div id="trialBanner" class="trial-banner" style="display:none;">
      <div class="trial-content">
        <span class="trial-icon">⏳</span>
        <div class="trial-text">
          <strong>Free Trial Active</strong>
          <span id="trialDays">Loading...</span>
        </div>
        <a href="/subscription" class="trial-btn">Subscribe Now</a>
      </div>
    </div>"""

new_banner = """<!-- FREE TRIAL BANNER -->
    <div id="trialBanner" class="trial-banner" style="display:none;">
      <div class="trial-content">
        <span class="trial-icon" id="trialIcon">⏳</span>
        <div class="trial-text">
          <strong id="trialTitle">Free Trial Active</strong>
          <span id="trialDays">Loading...</span>
        </div>
        <a href="/subscription" class="trial-btn">Subscribe Now</a>
      </div>
    </div>"""

html = html.replace(old_banner, new_banner)

# Replace the loadTrialInfo function with enhanced version
old_function = """// Free Trial Countdown Logic
    async function loadTrialInfo() {
      try {
        const res = await fetch('/api/auth/profile', { headers: auth });
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
    loadTrialInfo();"""

new_function = """// Enhanced Trial Countdown Logic
    async function loadTrialInfo() {
      try {
        const res = await fetch('/api/auth/profile', { headers: auth });
        if (res.ok) {
          const data = await res.json();
          if (data.subscriptionExpiryDate && !data.isSubscribed) {
            const expiry = new Date(data.subscriptionExpiryDate);
            const now = new Date();
            const diffDays = Math.ceil((expiry - now) / (1000 * 60 * 60 * 24));
            
            if (diffDays > 0) {
              const banner = document.getElementById('trialBanner');
              const icon = document.getElementById('trialIcon');
              const title = document.getElementById('trialTitle');
              const days = document.getElementById('trialDays');
              
              banner.style.display = 'block';
              days.textContent = diffDays + ' day' + (diffDays === 1 ? '' : 's') + ' remaining';
              
              // Change urgency based on days left
              if (diffDays <= 3) {
                banner.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
                icon.textContent = '🚨';
                title.textContent = 'Trial Ending Soon!';
              } else if (diffDays <= 7) {
                banner.style.background = 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)';
                icon.textContent = '⚠️';
                title.textContent = 'Trial Ending Soon';
              }
            }
          }
        }
      } catch(e) { console.error('Trial check failed:', e); }
    }
    loadTrialInfo();"""

html = html.replace(old_function, new_function)

with open('public/dashboard.html', 'w') as f:
    f.write(html)

print("✅ Trial reminder enhanced!")
