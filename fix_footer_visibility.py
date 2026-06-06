with open('public/index.html', 'r') as f:
    html = f.read()

# Add CSS to ensure the footer links are visible
css_fix = """
<style>
  body { padding-bottom: 50px !important; }
  .container, .card, .main-wrapper { height: auto !important; min-height: auto !important; }
</style>
"""

if '</head>' in html:
    html = html.replace('</head>', css_fix + '\n</head>')

with open('public/index.html', 'w') as f:
    f.write(html)
print("Footer visibility fixed!")
