with open('public/dashboard.html', 'r') as f:
    html = f.read()

# 1. Add CSS for the menu
css_code = """
<style>
  #hamburger-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 30px;
    background: none;
    border: none;
    cursor: pointer;
    color: #333;
    z-index: 1000;
  }
  #dropdown-menu {
    display: none;
    position: absolute;
    top: 60px;
    right: 20px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    z-index: 1000;
    min-width: 150px;
    flex-direction: column;
  }
  #dropdown-menu button, #dropdown-menu a {
    padding: 15px;
    text-align: left;
    background: none;
    border: none;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    font-size: 16px;
    color: #333;
    text-decoration: none;
    display: block;
  }
  #dropdown-menu button:last-child { border-bottom: none; }
  #dropdown-menu button:hover { background: #f9fafb; }
</style>
"""

# 2. Add HTML for the menu and JS to hide old buttons
menu_html = """
<div id="hamburger-btn">☰</div>
<div id="dropdown-menu">
  <button onclick="document.getElementById('watch-btn') ? document.getElementById('watch-btn').click() : alert('Watch feature')">Watch</button>
  <button onclick="window.location.href='/subscription'">Subscribe</button>
  <button onclick="toggleMode()">Mode</button>
  <button onclick="handleLogout()">Logout</button>
</div>

<script>
  // Hide old buttons
  document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
      if (btn.innerText.includes('Watch') || btn.innerText.includes('Subscribe') || btn.innerText.includes('Logout')) {
        btn.style.display = 'none';
      }
    });
    // Hide moon icon if it exists
    const icons = document.querySelectorAll('i, span');
    icons.forEach(icon => {
      if (icon.className && icon.className.includes('moon')) icon.style.display = 'none';
    });
  });

  // Toggle menu
  document.getElementById('hamburger-btn').addEventListener('click', () => {
    const menu = document.getElementById('dropdown-menu');
    menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
  });

  // Close menu when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target.id !== 'hamburger-btn' && !e.target.closest('#dropdown-menu')) {
      document.getElementById('dropdown-menu').style.display = 'none';
    }
  });
</script>
"""

# Inject CSS and HTML
if '</head>' in html:
    html = html.replace('</head>', css_code + '\n</head>')
if '<body' in html:
    html = html.replace('<body', menu_html + '\n<body')

with open('public/dashboard.html', 'w') as f:
    f.write(html)
print("Dashboard menu added!")
