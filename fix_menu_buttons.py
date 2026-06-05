with open('public/dashboard.html', 'r') as f:
    html = f.read()

# Fix the JavaScript to NOT hide buttons inside the dropdown menu
old_script = """buttons.forEach(btn => {
      if (btn.innerText.includes('Watch') || btn.innerText.includes('Subscribe') || btn.innerText.includes('Logout')) {
        btn.style.display = 'none';
      }
    });"""

new_script = """buttons.forEach(btn => {
      // Only hide buttons that are NOT inside the dropdown menu
      if (!btn.closest('#dropdown-menu')) {
        if (btn.innerText.includes('Watch') || btn.innerText.includes('Subscribe') || btn.innerText.includes('Logout')) {
          btn.style.display = 'none';
        }
      }
    });"""

html = html.replace(old_script, new_script)

with open('public/dashboard.html', 'w') as f:
    f.write(html)
print("Menu buttons fixed!")
