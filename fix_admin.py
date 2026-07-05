with open('public/admin.html', 'r') as f:
    html = f.read()

# Fix the users display to match actual database structure
old_users_code = """data.forEach(u => {
            let statusClass = u.subscription.status === 'active' ? 'badge-active' : (u.subscription.status === 'trial' ? 'badge-trial' : 'badge-expired');
            html += `<tr><td>${u.name}</td><td>${u.email}</td><td><span class="badge ${statusClass}">${u.subscription.status.toUpperCase()}</span></td></tr>`;
          });"""

new_users_code = """data.forEach(u => {
            let statusClass = u.isSubscribed ? 'badge-active' : 'badge-expired';
            let statusText = u.isSubscribed ? 'ACTIVE' : 'EXPIRED';
            html += `<tr><td>${u.name || 'No Name'}</td><td>${u.email || 'No Email'}</td><td><span class="badge ${statusClass}">${statusText}</span></td></tr>`;
          });"""

html = html.replace(old_users_code, new_users_code)

# Fix the laptops display to show owner name instead of "Unknown"
old_laptops_code = """data.forEach(l => {
            html += `<tr><td>${l.ownerName || 'Unknown'}</td><td>${l.brand} ${l.model}</td><td>${l.serialNumber}</td><td>${l.stolen ? '🚨 STOLEN' : ' ✅ Active'}</td></tr>`;
          });"""

new_laptops_code = """const ownerIds = [...new Set(data.map(l => l.user))];
            const ownerMap = {};
            for (const id of ownerIds) {
              try {
                const ownerRes = await fetch('/api/admin/user/' + id, { headers: { 'Authorization': 'Bearer ' + token } });
                if (ownerRes.ok) {
                  const ownerData = await ownerRes.json();
                  ownerMap[id] = ownerData.name || 'Unknown';
                }
              } catch (e) { ownerMap[id] = 'Unknown'; }
            }
            data.forEach(l => {
              const ownerName = ownerMap[l.user] || 'Unknown';
              html += `<tr><td>${ownerName}</td><td>${l.brand || 'Unknown'} ${l.model || ''}</td><td>${l.serialNumber || l.serial || 'Unknown'}</td><td>${l.stolen ? '🚨 STOLEN' : ' ✅ Active'}</td></tr>`;
            });"""

html = html.replace(old_laptops_code, new_laptops_code)

# Make the laptops loading function async
old_load_laptops = """else if (type === 'laptops') {
          document.getElementById('laptopCount').textContent = data.length;
          let html = '<table><thead><tr><th>Owner</th><th>Brand/Model</th><th>Serial</th><th>Status</th></tr></thead><tbody>';"""

new_load_laptops = """else if (type === 'laptops') {
          document.getElementById('laptopCount').textContent = data.length;
          let html = '<table><thead><tr><th>Owner</th><th>Brand/Model</th><th>Serial</th><th>Status</th></tr></thead><tbody>';"""

html = html.replace(old_load_laptops, new_load_laptops)

with open('public/admin.html', 'w') as f:
    f.write(html)

print("✅ Admin page fixed!")
