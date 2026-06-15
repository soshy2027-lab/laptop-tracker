with open('public/dashboard.html', 'r') as f:
    content = f.read()

# Fix 1: Wrap the modal button in a timeout so it doesn't crash if the HTML isn't ready yet
old_modal = "document.getElementById('confirmStolenBtn').onclick = () => {"
new_modal = "setTimeout(() => { document.getElementById('confirmStolenBtn').onclick = () => {"

# Fix 2: Close the timeout properly at the end of that function
old_end = "document.getElementById('obModal').style.display = 'none';\n    };"
new_end = "document.getElementById('obModal').style.display = 'none';\n    }; }, 100);"

# Fix 3: Make sure laptops load immediately
old_load = "document.addEventListener('DOMContentLoaded', loadData);"
new_load = "loadData();"

if old_modal in content and old_end in content:
    content = content.replace(old_modal, new_modal, 1)
    content = content.replace(old_end, new_end, 1)
    content = content.replace(old_load, new_load, 1)
    
    with open('public/dashboard.html', 'w') as f:
        f.write(content)
    print("Fixed the crash and loading issue!")
else:
    print("Could not find the exact code. Please run: sed -n '570,585p' public/dashboard.html and reply with the output.")
