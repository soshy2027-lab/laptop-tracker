with open('server.js', 'r') as f:
    code = f.read()

# Fix the critical bug where false || true = true
old_code = "{ stolen: req.body.stolen || true, status: req.body.stolen ? 'Stolen' : 'Active' }"
new_code = "{ stolen: req.body.stolen, status: req.body.stolen ? 'Stolen' : 'Active' }"

if old_code in code:
    code = code.replace(old_code, new_code)
    with open('server.js', 'w') as f:
        f.write(code)
    print("Safe button bug fixed!")
else:
    print("Code pattern not found!")
