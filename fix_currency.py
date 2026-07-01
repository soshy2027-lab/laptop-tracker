with open('server.js', 'r') as f:
    server = f.read()

# Fix the order data to ensure currency_code is at the root level
old_order = """const orderData = {
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

new_order = """const orderData = {
      id: 'LAPTOP_' + Date.now(),
      type: 'MERCHANT',
      currency: 'KES',
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

print("✅ Currency code format fixed!")
