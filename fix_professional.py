with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Fix form title
content = content.replace('<h2>Add New Laptop</h2>', '<h2>Add New Device</h2>')

# 2. Fix button text dynamically
old_btn = '<button type="submit" class="btn-add">Add Laptop</button>'
new_btn = '<button type="submit" class="btn-add" id="addBtn">Add Device</button>'
content = content.replace(old_btn, new_btn)

# 3. Add script to change button text based on dropdown
dropdown_script = """
    // Update button text based on device type
    const deviceTypeSelect = document.getElementById('deviceType');
    const addBtn = document.getElementById('addBtn');
    if(deviceTypeSelect && addBtn) {
      deviceTypeSelect.addEventListener('change', function() {
        addBtn.textContent = this.value === 'Phone' ? 'Add Phone' : 'Add Laptop';
      });
    }
"""
content = content.replace('</script>', dropdown_script + '</script>', 1)

# 4. Fix the Police Report function - remove the broken one and add clean version
if 'window.generatePoliceReport' in content:
    # Remove old broken function
    import re
    content = re.sub(r'window\.generatePoliceReport.*?};', '', content, flags=re.DOTALL)

# 5. Add clean Police Report function before closing body tag
police_func = """
<script>
window.generatePoliceReport = function(id) {
  const l = laptops.find(x => String(x._id) === id);
  if(!l) return;
  
  const reportHTML = `<!DOCTYPE html>
<html>
<head>
  <title>Police Report - ${l.brand} ${l.model}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; background: #fff; color: #111; line-height: 1.6; }
    .header { background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
    .header h1 { font-size: 28px; margin-bottom: 10px; }
    .header p { opacity: 0.9; font-size: 14px; }
    .section { background: #f9fafb; padding: 25px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #dc2626; }
    .section h2 { color: #dc2626; margin-bottom: 15px; font-size: 20px; }
    .info-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #e5e7eb; }
    .info-row:last-child { border-bottom: none; }
    .label { font-weight: 600; color: #374151; }
    .value { color: #111827; font-weight: 500; }
    .footer { margin-top: 40px; padding: 20px; background: #f3f4f6; border-radius: 8px; text-align: center; color: #6b7280; font-size: 14px; }
    .badge { display: inline-block; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 600; }
    .badge-laptop { background: #dbeafe; color: #1e40af; }
    .badge-phone { background: #fef3c7; color: #92400e; }
    @media print { body { padding: 20px; } .header { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
  </style>
</head>
<body>
  <div class="header">
    <h1>🚨 STOLEN DEVICE POLICE REPORT</h1>
    <p>Official Tracking Document - Laptop Tracker System</p>
  </div>
  
  <div class="section">
    <h2>📋 Report Information</h2>
    <div class="info-row"><span class="label">Date Generated:</span><span class="value">${new Date().toLocaleString()}</span></div>
    <div class="info-row"><span class="label">Device Type:</span><span class="value"><span class="badge ${l.deviceType === 'Phone' ? 'badge-phone' : 'badge-laptop'}">${l.deviceType === 'Phone' ? '📱 Phone' : '💻 Laptop'}</span></span></div>
  </div>
  
  <div class="section">
    <h2> Device Details</h2>
    <div class="info-row"><span class="label">Brand:</span><span class="value">${l.brand}</span></div>
    <div class="info-row"><span class="label">Model:</span><span class="value">${l.model}</span></div>
    <div class="info-row"><span class="label">Serial Number:</span><span class="value">${l.serial}</span></div>
    <div class="info-row"><span class="label">RAM:</span><span class="value">${l.ram}</span></div>
    <div class="info-row"><span class="label">Storage:</span><span class="value">${l.storage}</span></div>
  </div>
  
  <div class="section">
    <h2>👮 Police Report Details</h2>
    <div class="info-row"><span class="label">OB Number:</span><span class="value">${l.obNumber || 'Not provided'}</span></div>
    <div class="info-row"><span class="label">Police Station:</span><span class="value">${l.policeStation || 'Not provided'}</span></div>
    <div class="info-row"><span class="label">Report Date:</span><span class="value">${l.reportDate ? new Date(l.reportDate).toLocaleDateString() : 'Not provided'}</span></div>
  </div>
  
  <div class="section">
    <h2>📍 Tracking Information</h2>
    <div class="info-row"><span class="label">Last Seen:</span><span class="value">${l.lastSeen ? new Date(l.lastSeen).toLocaleString() : 'Never'}</span></div>
    <div class="info-row"><span class="label">Last IP Address:</span><span class="value">${l.lastIpAddress || 'Unknown'}</span></div>
    <div class="info-row"><span class="label">Last Location:</span><span class="value">${l.lastLocation && l.lastLocation.city ? l.lastLocation.city + ', ' + l.lastLocation.country : 'Unknown'}</span></div>
  </div>
  
  <div class="footer">
    <p><strong>This report was automatically generated by Laptop Tracker.</strong></p>
    <p>Please present this document to your local law enforcement agency to assist in the recovery of your device.</p>
    <p style="margin-top: 15px; font-size: 12px;">Report ID: ${l._id}</p>
  </div>
  
  <script>window.onload = function() { window.print(); }<\\/script>
</body>
</html>`;
  
  const win = window.open('', '_blank');
  win.document.write(reportHTML);
  win.document.close();
};
</script>
"""

content = content.replace('</body>', police_func + '</body>', 1)

with open('public/dashboard.html', 'w') as f:
    f.write(content)

print("✅ Professional fixes applied! Police Report will render beautifully.")
