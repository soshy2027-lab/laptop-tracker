with open('public/dashboard.html', 'r') as f:
    content = f.read()

# 1. Fix the API endpoint for the trial banner
content = content.replace("fetch('/api/profile'", "fetch('/api/auth/profile'")

# 2. Make the install button always visible by default
content = content.replace('id="installBtn" style="display:none;"', 'id="installBtn"')

# 3. Replace the install button logic with better version
old_install_js = """    // PWA Install Button Logic
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
    };"""

new_install_js = """    // PWA Install Button Logic
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
    });

    window.installApp = async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
          alert('✅ App installed successfully!');
        }
        deferredPrompt = null;
      } else {
        // Show manual installation instructions
        alert('To install the app:\\n\\n**On Android (Chrome):**\\n1. Tap the 3 dots (⋮) in top right\\n2. Tap "Install app" or "Add to Home screen"\\n\\n**On iPhone (Safari):**\\n1. Tap the Share button (□↑)\\n2. Tap "Add to Home Screen"\\n3. Tap "Add"');
      }
    };"""

content = content.replace(old_install_js, new_install_js)

with open('public/dashboard.html', 'w') as f:
    f.write(content)

print("✅ Fixed! Banner will show correctly, and Install button is always visible with manual instructions.")
