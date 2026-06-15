with open('public/dashboard.html', 'r') as f:
    content = f.read()

modal_html = """
<!-- OB Number Modal -->
<div id="obModal" style="display:none; position:fixed; z-index:1000; left:0; top:0; width:100%; height:100%; background-color:rgba(0,0,0,0.6);">
  <div style="background:#fff; margin:15% auto; padding:20px; border-radius:8px; width:90%; max-width:400px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
    <h3 style="margin-top:0; color:#dc2626;"> Report Stolen Laptop</h3>
    <p style="font-size:14px; color:#555;">Please enter the details from your police report to activate tracking.</p>
    <label style="display:block; margin-top:10px; font-weight:bold; font-size:14px;">Police Station Name</label>
    <input type="text" id="obPoliceStation" style="width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" placeholder="e.g. Central Police Station">
    
    <label style="display:block; margin-top:10px; font-weight:bold; font-size:14px;">OB Number</label>
    <input type="text" id="obNumber" style="width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" placeholder="e.g. OB 123/06/2026">
    
    <label style="display:block; margin-top:10px; font-weight:bold; font-size:14px;">Date of Report</label>
    <input type="date" id="obDate" style="width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;">
    
    <div style="margin-top:20px; display:flex; justify-content:space-between;">
      <button onclick="document.getElementById('obModal').style.display='none'" style="padding:10px 15px; background:#ccc; border:none; border-radius:4px; cursor:pointer;">Cancel</button>
      <button id="confirmStolenBtn" style="padding:10px 15px; background:#dc2626; color:white; border:none; border-radius:4px; cursor:pointer;">Confirm Stolen</button>
    </div>
  </div>
</div>
</body>"""

if "</body>" in content:
    content = content.replace("</body>", modal_html)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("Modal HTML added successfully!")
else:
    print("Could not find </body> tag!")
