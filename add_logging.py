with open('server.js', 'r') as f:
    server = f.read()

# Add detailed logging to the Pesapal endpoint
old_code = """app.post('/api/pesapal/submit-order', protect, async (req, res) => {
  try {
    const token = await getPesapalToken();"""

new_code = """app.post('/api/pesapal/submit-order', protect, async (req, res) => {
  try {
    console.log('=== PESAPAL REQUEST STARTED ===');
    console.log('User ID:', req.user._id);
    console.log('Consumer Key:', PESAPAL_CONSUMER_KEY);
    console.log('Base URL:', PESAPAL_BASE_URL);
    
    const token = await getPesapalToken();
    console.log('✅ Got Pesapal token');"""

server = server.replace(old_code, new_code)

# Add more logging after getting token
old_response = """const response = await axios.post(`${PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest`, orderData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json', Accept: 'application/json' }
    });
    res.json({ redirect_url: response.data.RedirectURL });"""

new_response = """console.log('Sending order to Pesapal...');
    console.log('Order data:', JSON.stringify(orderData, null, 2));
    
    const response = await axios.post(`${PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest`, orderData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json', Accept: 'application/json' }
    });
    
    console.log('✅ Pesapal response:', response.data);
    res.json({ redirect_url: response.data.RedirectURL });"""

server = server.replace(old_response, new_response)

# Add error logging
old_error = """} catch (err) {
    res.status(500).json({ 
      error: 'Pesapal failed', 
      details: err.response?.data || err.message,
      status: err.response?.status 
    });"""

new_error = """} catch (err) {
    console.log('❌ PESAPAL ERROR:', err.message);
    console.log('❌ Error details:', err.response?.data);
    console.log('❌ Error status:', err.response?.status);
    res.status(500).json({ 
      error: 'Pesapal failed', 
      details: err.response?.data || err.message,
      status: err.response?.status 
    });"""

server = server.replace(old_error, new_error)

with open('server.js', 'w') as f:
    f.write(server)

print("✅ Detailed logging added!")
