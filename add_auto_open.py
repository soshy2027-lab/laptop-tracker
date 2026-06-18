with open('public/dashboard.html', 'r') as f:
    content = f.read()

old_block = """      if(res.ok) {
        const deviceType = document.getElementById('deviceType').value;
        const msgText = deviceType === 'Phone' ? '✅ Phone added successfully!' : '✅ Laptop added successfully!';
        document.getElementById('msg').textContent = msgText;
        setTimeout(()=>document.getElementById('msg').textContent='', 3000);
        e.target.reset();
        loadData();
      }"""

new_block = """      if(res.ok) {
        const newDevice = await res.json(); // Get the new device ID from server
        const deviceType = document.getElementById('deviceType').value;
        const msgText = deviceType === 'Phone' ? '✅ Phone added successfully!' : '✅ Laptop added successfully!';
        document.getElementById('msg').textContent = msgText;
        setTimeout(()=>document.getElementById('msg').textContent='', 3000);
        e.target.reset();
        loadData();
        // Automatically open tracker page with ID filled in
        window.open('/tracker.html?id=' + newDevice._id, '_blank');
      }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ Auto-open tracker added safely!")
else:
    print("❌ Could not find the exact code.")
