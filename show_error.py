with open('public/subscription.html', 'r') as f:
    html = f.read()

# Change the alert to show the full error details from the server
html = html.replace("alert(data.error || 'Pesapal failed');", "alert('ERROR: ' + JSON.stringify(data));")

with open('public/subscription.html', 'w') as f:
    f.write(html)

print("✅ Frontend updated to show real error!")
