with open('public/dashboard.html', 'r') as f:
    content = f.read()

old_func = """    window.toggleStolen = async (id, stolen) => {
      const confirmMsg = stolen
        ? '🚨 MARK AS STOLEN?\\n\\nThis will alert the admin and track the last known location.'
        : '✅ Mark this laptop as safe?';
      if (!confirm(confirmMsg)) return;
      try {
        const res = await fetch(`/api/laptops/${id}/stolen`, {
          method: 'PUT',
          headers: { ...auth, 'Content-Type': 'application/json' },
          body: JSON.stringify({ stolen })
        });
        if (res.ok) {
          alert(stolen ? ' Laptop marked as STOLEN!' : '✅ Laptop marked as safe.');
          loadData();
        } else alert('Failed: ' + (await res.json()).error);
      } catch (err) {
        alert('Error: ' + err.message);
      }
    };"""

new_func = """    let pendingStolenId = null;

    window.toggleStolen = (id, stolen) => {
      if (!stolen) {
        if (!confirm('✅ Mark this laptop as safe?')) return;
        sendStolenUpdate(id, false);
      } else {
        pendingStolenId = id;
        document.getElementById('obDate').value = new Date().toISOString().split('T')[0];
        document.getElementById('obModal').style.display = 'block';
      }
    };

    document.getElementById('confirmStolenBtn').onclick = () => {
      const obNumber = document.getElementById('obNumber').value.trim();
      const policeStation = document.getElementById('obPoliceStation').value.trim();
      const reportDate = document.getElementById('obDate').value;

      if (!obNumber || !policeStation || !reportDate) {
        alert('Please fill in all police report details to proceed.');
        return;
      }

      sendStolenUpdate(pendingStolenId, true, obNumber, policeStation, reportDate);
      document.getElementById('obModal').style.display = 'none';
    };

    async function sendStolenUpdate(id, stolen, obNumber = '', policeStation = '', reportDate = '') {
      try {
        const res = await fetch(`/api/laptops/${id}/stolen`, {
          method: 'PUT',
          headers: { ...auth, 'Content-Type': 'application/json' },
          body: JSON.stringify({ stolen, obNumber, policeStation, reportDate })
        });
        if (res.ok) {
          alert(stolen ? '🚨 Laptop marked as STOLEN! Tracking activated.' : '✅ Laptop marked as safe.');
          loadData();
        } else alert('Failed: ' + (await res.json()).error);
      } catch (err) {
        alert('Error: ' + err.message);
      }
    }"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("JavaScript updated successfully!")
else:
    print("Could not find the old function to replace!")
