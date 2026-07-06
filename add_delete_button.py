with open('public/admin.html', 'r') as f:
    html = f.read()

# Find the users table row and add delete button
old_users_row = """html += `<tr><td>${u.name || 'No Name'}</td><td>${u.email || 'No Email'}</td><td><span class="badge ${statusClass}">${statusText}</span></td></tr>`;"""

new_users_row = """html += `<tr><td>${u.name || 'No Name'}</td><td>${u.email || 'No Email'}</td><td><span class="badge ${statusClass}">${statusText}</span></td><td><button onclick="deleteUser('${u._id}', '${u.name}')" style="background:#dc2626;color:white;border:none;padding:4px 8px;border-radius:4px;cursor:pointer;font-size:0.75rem;">Delete</button></td></tr>`;"""

html = html.replace(old_users_row, new_users_row)

# Add deleteUser function before the closing script tag
delete_function = """
    window.deleteUser = (userId, userName) => {
      if (!confirm(`⚠️ Are you sure you want to delete user "${userName}"?\\n\\nThis will also delete all their laptops. This action cannot be undone!`)) return;
      
      fetch('/api/admin/user/' + userId, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + token }
      })
      .then(res => res.json())
      .then(data => {
        alert('✅ ' + data.message);
        loadData('users');
      })
      .catch(err => {
        alert('❌ Error deleting user: ' + err.message);
      });
    };
"""

html = html.replace('</script>', delete_function + '</script>')

with open('public/admin.html', 'w') as f:
    f.write(html)

print("✅ Delete button added!")
