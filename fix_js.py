with open('public/dashboard.html', 'r') as f:
    content = f.read()

start_str = 'window.toggleStolen = async (id, stolen) => {'
start_idx = content.find(start_str)

if start_idx == -1:
    print("Could not find the start of the function!")
else:
    err_alert_str = "alert('Error: ' + err.message);"
    err_idx = content.find(err_alert_str, start_idx)
    
    if err_idx == -1:
        print("Could not find the end of the function!")
    else:
        end_search_str = content[err_idx:err_idx+100]
        end_idx = end_search_str.rfind('};')
        if end_idx == -1:
            print("Could not find the closing braces!")
        else:
            actual_end_idx = err_idx + end_idx + 2
            
            new_func = """let pendingStolenId = null;

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
          alert(stolen ? ' Laptop marked as STOLEN! Tracking activated.' : '✅ Laptop marked as safe.');
          loadData();
        } else alert('Failed: ' + (await res.json()).error);
      } catch (err) {
        alert('Error: ' + err.message);
      }
    }"""

            content = content[:start_idx] + new_func + content[actual_end_idx:]
            with open('public/dashboard.html', 'w') as f:
                f.write(content)
            print("JavaScript updated successfully!")
