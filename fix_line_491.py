with open('public/dashboard.html', 'r') as f:
    lines = f.readlines()

# We know exactly it's line 491 (index 490)
target_index = 490
if target_index < len(lines) and "deviceType === 'Phone'" in lines[target_index]:
    # Replace ONLY this line with clean text that fits your dark theme
    lines[target_index] = "            <td style=\"font-weight:bold; color:#e5e7eb;\">${l.deviceType === 'Phone' ? '📱 Phone' : '💻 Laptop'}</td>\n"
    
    with open('public/dashboard.html', 'w') as f:
        f.writelines(lines)
    print("✅ Line 491 updated safely! White box removed.")
else:
    print("❌ Could not find the exact line.")
