with open('server.js', 'r') as f:
    code = f.read()

code = code.replace(
    "const mapUrl = laptop.lastLocation?.latitude ? 'https://maps.google.com?q=' + laptop.lastLocation.latitude + ',' + laptop.lastLocation.longitude : 'No location data';",
    "const mapUrl = laptop.lastLocation?.latitude ? 'https://maps.google.com?q=' + laptop.lastLocation.latitude + ',' + laptop.lastLocation.longitude : '#';"
)

with open('server.js', 'w') as f:
    f.write(code)
print("Fixed!")
