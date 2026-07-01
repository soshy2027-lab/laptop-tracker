with open('server.js', 'r') as f:
    server = f.read()

# Fix the order data format
old_order = """const orderData = {
      id: req.user._id.toString(),
      currency_code: 'KES',
      amount: 2500,
      description: 'Laptop Tracker Subscription',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      notification_id: '',
      ordering_reference: 'LAPTOP_' + Date.now(),
      meta_data: [{ key: 'user_id', value: req.user._id.toString() }],
      items: [{ title: 'Subscription', quantity: 1, unit_cost: 2500 }]
    };"""

new_order = """const orderData = {
      id: 'LAPTOP_' + Date.now(),
      currency_code: 'KES',
      amount: 2500.00,
      description: 'Laptop Tracker Subscription - 4 Months',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      notification_id: '',
      ordering_reference: 'LAPTOP_' + Date.now(),
      meta_data: [],
      items: [
        {
          title: 'Laptop Tracker Subscription',
          description: '4 months unlimited tracking',
          unit_cost: 2500.00,
          quantity: 1,
          sku_code: 'LAPTOP_SUB_4M',
          tax: 0.00
        }
      ]
    };"""

server = server.replace(old_order, new_order)

with open('server.js', 'w') as f:
    f.write(server)

print("✅ Pesapal order format fixed!")
