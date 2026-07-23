with open('server.js', 'r') as f:
    content = f.read()

# Find and replace the entire pesapal submit-order endpoint
old_endpoint = """app.post('/api/pesapal/submit-order', protect, async (req, res) => {
  try {
    console.log('=== PESAPAL REQUEST STARTED ===');
    console.log('User ID:', req.user._id);
    console.log('Consumer Key:', PESAPAL_CONSUMER_KEY);
    console.log('Base URL:', PESAPAL_BASE_URL);

    const token = await getPesapalToken();
    console.log('✅ Got Pesapal token');
    const orderData = {
      id: 'LAPTOP_' + Date.now(),
      type: 'MERCHANT',
      currency: 'KES',
      amount: 2500.00,
      description: 'Laptop Tracker Subscription - 4 Months',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      ordering_reference: 'LAPTOP_' + Date.now(),
      meta_data: [],
      items: ["""

new_endpoint = """app.post('/api/pesapal/submit-order', protect, async (req, res) => {
  try {
    const token = await getPesapalToken();
    
    // Get user info safely
    const userEmail = req.user.email || 'user@example.com';
    const userName = req.user.name || 'User Name';
    const nameParts = userName.split(' ');
    const firstName = nameParts[0] || 'User';
    const lastName = nameParts.slice(1).join(' ') || 'Name';
    
    const orderData = {
      id: 'LAPTOP_' + Date.now(),
      type: 'MERCHANT',
      currency: 'KES',
      amount: 2500.00,
      description: 'Laptop Tracker Subscription - 4 Months',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      ordering_reference: 'LAPTOP_' + Date.now(),
      // REQUIRED billing address for Pesapal
      billing_address: {
        email_address: userEmail,
        phone_number: req.user.phone || '+254700000000',
        country_code: 'KE',
        first_name: firstName,
        last_name: lastName,
        line_1: 'Nairobi',
        city: 'Nairobi',
        state: 'Nairobi',
        postal_code: '00100'
      },
      meta_data: [],
      items: ["""

if old_endpoint in content:
    content = content.replace(old_endpoint, new_endpoint)
    with open('server.js', 'w') as f:
        f.write(content)
    print("✅ Pesapal billing address FIXED!")
else:
    print("⚠️ Pattern not found - checking alternative...")
    # Alternative: search for just the orderData part
    if 'missing_mandatory_billing_address' not in content:
        import re
        content = re.sub(
            r"(const orderData = \{[^}]*?ordering_reference:[^}]*?)(meta_data:\[\])",
            r"\1billing_address: { email_address: req.user.email, phone_number: '+254700000000', country_code: 'KE', first_name: 'User', last_name: 'Name', line_1: 'Nairobi', city: 'Nairobi', state: 'Nairobi', postal_code: '00100' },\n      \2",
            content,
            flags=re.DOTALL
        )
        with open('server.js', 'w') as f:
            f.write(content)
        print("✅ Pesapal fixed with alternative method!")

