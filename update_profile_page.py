with open('public/profile.html', 'r') as f:
    html = f.read()

# Replace the placeholder script with real API fetch
old_script = """  <script>
    // Simple script to show placeholder data for now
    document.getElementById('profileName').textContent = 'Laptop Tracker User';
    document.getElementById('profileEmail').textContent = 'user@example.com';
    document.getElementById('profilePhone').textContent = '+254 700 000 000';
    document.getElementById('profileDate').textContent = 'June 2026';
  </script>"""

new_script = """  <script>
    // Fetch real user data from API
    async function loadProfile() {
      const token = localStorage.getItem('token');
      
      if (!token) {
        alert('Please login first');
        window.location.href = '/login.html';
        return;
      }

      try {
        const response = await fetch('/api/auth/profile', {
          headers: {
            'Authorization': 'Bearer ' + token
          }
        });

        if (!response.ok) {
          throw new Error('Failed to load profile');
        }

        const user = await response.json();
        
        // Update profile with real data
        document.getElementById('profileName').textContent = user.name || 'User';
        document.getElementById('profileEmail').textContent = user.email || 'Not provided';
        document.getElementById('profilePhone').textContent = user.phone || 'Not provided';
        
        // Format date
        const joinDate = new Date(user.memberSince);
        document.getElementById('profileDate').textContent = joinDate.toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'long' 
        });
        
        // Update avatar initials
        const initials = user.name ? user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) : 'U';
        document.getElementById('avatarInitials').textContent = initials;
        
        // Update subscription status
        const statusBadge = document.getElementById('profileStatus');
        if (user.isSubscribed) {
          statusBadge.textContent = 'Premium Active';
          statusBadge.className = 'status-badge status-premium';
        } else if (user.trialEndDate && new Date(user.trialEndDate) > new Date()) {
          statusBadge.textContent = 'Free Trial (21 Days)';
          statusBadge.className = 'status-badge status-free';
        } else {
          statusBadge.textContent = 'Free Tier';
          statusBadge.className = 'status-badge status-free';
        }
        
      } catch (error) {
        console.error('Profile load error:', error);
        alert('Error loading profile. Please login again.');
        window.location.href = '/login.html';
      }
    }

    // Load profile on page load
    loadProfile();
  </script>"""

if old_script in html:
    html = html.replace(old_script, new_script)
    with open('public/profile.html', 'w') as f:
        f.write(html)
    print("Profile page updated to fetch real data!")
else:
    print("Could not find script to replace!")
