with open('public/dashboard.html', 'r') as f:
    content = f.read()

# Make all text in the modal bold and dark
old_modal = """<h3 style="margin-top:0; color:#dc2626;"> Report Stolen Laptop</h3>
    <p style="font-size:14px; color:#555;">Please enter the details from your police report to activate tracking.</p>
    <label style="display:block; margin-top:10px; font-weight:bold; font-size:14px;">Police Station Name</label>
    <input type="text" id="obPoliceStation" style="width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" placeholder="e.g. Central Police Station">
    
    <label style="display:block; margin-top:10px; font-weight:bold; font-size:14px;">OB Number</label>
    <input type="text" id="obNumber" style="width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" placeholder="e.g. OB 123/06/2026">
    
    <label style="display:block; margin-top:10px; font-weight:bold; font-size:14px;">Date of Report</label>
    <input type="date" id="obDate" style="width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;">"""

new_modal = """<h3 style="margin-top:0; color:#dc2626; font-weight:bold; font-size:22px;">🚨 Report Stolen Laptop</h3>
    <p style="font-size:15px; color:#1f2937; font-weight:600;">Please enter the details from your police report to activate tracking.</p>
    <label style="display:block; margin-top:15px; font-weight:bold; font-size:15px; color:#111827;">📍 Police Station Name</label>
    <input type="text" id="obPoliceStation" style="width:100%; padding:10px; margin-top:5px; border:2px solid #d1d5db; border-radius:6px; box-sizing:border-box; font-size:15px; font-weight:500;" placeholder="e.g. Central Police Station">
    
    <label style="display:block; margin-top:15px; font-weight:bold; font-size:15px; color:#111827;">📋 OB Number</label>
    <input type="text" id="obNumber" style="width:100%; padding:10px; margin-top:5px; border:2px solid #d1d5db; border-radius:6px; box-sizing:border-box; font-size:15px; font-weight:500;" placeholder="e.g. OB 123/06/2026">
    
    <label style="display:block; margin-top:15px; font-weight:bold; font-size:15px; color:#111827;">📅 Date of Report</label>
    <input type="date" id="obDate" style="width:100%; padding:10px; margin-top:5px; border:2px solid #d1d5db; border-radius:6px; box-sizing:border-box; font-size:15px; font-weight:500;">"""

if old_modal in content:
    content = content.replace(old_modal, new_modal)
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("✅ OB form text fixed - now bold and visible!")
else:
    print("❌ Could not find the modal to update")
