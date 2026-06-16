with open('public/index.html', 'r') as f:
    content = f.read()

sw_script = """
<script>
  // Register Service Worker for PWA Install Prompt
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then(reg => console.log('SW registered'))
        .catch(err => console.log('SW error:', err));
    });
  }
</script>
</body>"""

if "</body>" in content:
    content = content.replace("</body>", sw_script)
    with open('public/index.html', 'w') as f:
        f.write(content)
    print("✅ Service Worker registered! Users will now see the Install App popup.")
else:
    print("❌ Could not find </body> tag")
