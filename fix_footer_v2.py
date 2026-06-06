with open('public/index.html', 'r') as f:
    html = f.read()

css_fix = """
<style>
  html, body { height: auto !important; overflow-y: auto !important; }
  .container, .card, .main-wrapper, .auth-box, .login-container, div[style*="background: white"] { 
    height: auto !important; 
    max-height: none !important; 
    min-height: auto !important; 
    overflow: visible !important; 
  }
  .footer-links { margin-bottom: 20px !important; }
</style>
"""

# Remove old fix if it exists to avoid clutter
html = html.replace('<style>\n  body { padding-bottom: 50px !important; }\n  .container, .card, .main-wrapper { height: auto !important; min-height: auto !important; }\n</style>\n', '')

if '</head>' in html:
    html = html.replace('</head>', css_fix + '\n</head>')

with open('public/index.html', 'w') as f:
    f.write(html)
print("Footer visibility fixed v2!")
