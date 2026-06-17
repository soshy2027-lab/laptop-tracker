with open('public/dashboard.html', 'r') as f:
    content = f.read()

# Remove the old duplicate buttons that are causing conflicts
old_buttons = """        <button class="btn btn-sub" onclick="window.location.href='/subscription'"> Subscribe</button>
        <button class="btn btn-theme" id="themeToggle" onclick="toggleTheme()">🌙</button>
        <button class="btn btn-logout" onclick="logout()">Logout</button>"""

if old_buttons in content:
    content = content.replace(old_buttons, "", 1)
    print("✅ Removed old duplicate buttons!")
else:
    print("⚠️ Old buttons not found, checking for variations...")
    # Try to find them with different spacing
    import re
    pattern = r'<button class="btn btn-sub".*?</button>\s*<button class="btn btn-theme".*?</button>\s*<button class="btn btn-logout".*?</button>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    print("✅ Removed old buttons using pattern matching!")

# Remove the hiding script since we don't need it anymore
old_script = """  // Hide old buttons
  document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
      // Only hide buttons that are NOT inside the dropdown menu
      if (!btn.closest('#dropdown-menu')) {
        if (btn.innerText.includes('Watch') || btn.innerText.includes('Subscribe') || btn.innerText.includes('Logout')) {
          btn.style.display = 'none';
        }
      }
    });
    // Hide moon icon if it exists
    const icons = document.querySelectorAll('i, span');
    icons.forEach(icon => {
      if (icon.className && icon.className.includes('moon')) icon.style.display = 'none';
    });
  });"""

if old_script in content:
    content = content.replace(old_script, "", 1)
    print("✅ Removed old hiding script!")

with open('public/dashboard.html', 'w') as f:
    f.write(content)
print("✅ Menu fixed! Your dropdown will now work perfectly!")
