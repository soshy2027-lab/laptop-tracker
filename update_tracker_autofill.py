with open('public/tracker.html', 'r') as f:
    content = f.read()

script = """
<script>
  // Auto-fill ID from URL
  const urlParams = new URLSearchParams(window.location.search);
  const deviceId = urlParams.get('id');
  if (deviceId) {
    document.getElementById('laptopId').value = deviceId;
  }
</script>
"""

if '</body>' in content:
    content = content.replace('</body>', script + '</body>')
    with open('public/tracker.html', 'w') as f:
        f.write(content)
    print("✅ Tracker page updated to auto-fill ID!")
else:
    print("❌ Could not find body tag.")
