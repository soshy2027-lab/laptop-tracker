with open('server.js', 'r') as f:
    server_code = f.read()

# Find the orderData object and add billing address
old_order_data = """const orderData = {
      id: 'LAPTOP_' + Date.now(),
      type: 'MERCHANT',
      currency: 'KES',
      amount: 2500.00,
      description: 'Laptop Tracker Subscription - 4 Months',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      ordering_reference: 'LAPTOP_' + Date.now(),
      meta_data: [],
      items: ["""

new_order_data = """const orderData = {
      id: 'LAPTOP_' + Date.now(),
      type: 'MERCHANT',
      currency: 'KES',
      amount: 2500.00,
      description: 'Laptop Tracker Subscription - 4 Months',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      ordering_reference: 'LAPTOP_' + Date.now(),
      // Add required billing address
      billing_address: {
        email_address: req.user.email || 'user@example.com',
        phone_number: req.user.phone || '+254700000000',
        country_code: 'KE',
        first_name: req.user.name?.split(' ')[0] || 'User',
        last_name: req.user.name?.split(' ').slice(1).join(' ') || 'Name',
        line_1: 'Nairobi',
        line_2: 'Kenya',
        city: 'Nairobi',
        state: 'Nairobi',
        postal_code: '00100',
        zip_code: '00100'
      },
      meta_data: [],
      items: ["""

server_code = server_code.replace(old_order_data, new_order_data)

with open('server.js', 'w') as f:
    f.write(server_code)

print("✅ Added billing address to Pesapal request!")
