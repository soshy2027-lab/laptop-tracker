with open('public/subscription.html', 'r') as f:
    content = f.read()

old_paypal = """    // 💳 PayPal Payment
    paypal.Buttons({
      createOrder: async () => {
        try {
          const res = await fetch('/api/paypal/create-order', { method: 'POST', headers: auth });
          const data = await res.json();
          return data.id;
        } catch (err) { showError('Failed to create PayPal order'); }
      },"""

new_paypal = """    // 💳 PayPal Payment
    paypal.Buttons({
      createOrder: async () => {
        try {
          const res = await fetch('/api/paypal/create-order', { method: 'POST', headers: auth });
          const data = await res.json();
          console.log('PayPal Order Response:', data);
          if (!res.ok) {
            showError(data.error || 'Server error creating order');
            throw new Error(data.error || 'Server error');
          }
          if (!data.id) {
            showError('Invalid response from server');
            throw new Error('No order ID');
          }
          return data.id;
        } catch (err) { 
          console.error('PayPal createOrder error:', err);
          showError('Failed to create PayPal order: ' + err.message);
          throw err;
        }
      },"""

if old_paypal in content:
    content = content.replace(old_paypal, new_paypal)
    with open('public/subscription.html', 'w') as f:
        f.write(content)
    print("✅ PayPal error handling added! Now we'll see the real error.")
else:
    print("❌ Could not find the exact PayPal code.")
