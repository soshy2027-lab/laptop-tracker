with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Add the Install button HTML after Profile button
old_menu = """  <button onclick="window.location.href='/profile'">Profile</button>
  <button onclick="window.location.href='/dashboard'">Homepage</button>"""

new_menu = """  <button onclick="window.location.href='/profile'">Profile</button>
  <button id="installBtn" style="display:none;" onclick="installApp()">📱 Install App</button>
  <button onclick="window.location.href='/dashboard'">Homepage</button>"""

if old_menu in content:
    content = content.replace(old_menu, new_menu)
else:
    print("❌ Could not find menu code")
    exit()

# 2. Add the JavaScript to handle the install prompt
install_js = """
    // PWA Install Button Logic
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      document.getElementById('installBtn').style.display = 'block';
    });

    window.installApp = async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
          document.getElementById('installBtn').style.display = 'none';
        }
        deferredPrompt = null;
      }
    };
"""

# Insert the JavaScript before the closing </script> tag
if '</script>' in content:
    content = content.replace('</script>', install_js + '</script>', 1)
else:
    print("❌ Could not find script tag")
    exit()

with open('public/dashboard.html', 'w') as f:
    f.write(content)

print("✅ Install button added safely! It will only show for users who haven't installed the app.")
