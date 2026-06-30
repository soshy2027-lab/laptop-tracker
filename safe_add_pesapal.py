import os

# 1. Update server.js SAFELY (Only adds, never deletes)
with open('server.js', 'r') as f:
    server = f.read()

pesapal_server_code = """
// --- PESAPAL INTEGRATION ---
const PESAPAL_CONSUMER_KEY = process.env.PESAPAL_CONSUMER_KEY;
const PESAPAL_CONSUMER_SECRET = process.env.PESAPAL_CONSUMER_SECRET;
const PESAPAL_BASE_URL = 'https://cybqa.pesapal.com/pesapalv3';

async function getPesapalToken() {
  const res = await axios.post(`${PESAPAL_BASE_URL}/api/Auth/RequestToken`, {
    consumer_key: PESAPAL_CONSUMER_KEY,
    consumer_secret: PESAPAL_CONSUMER_SECRET
  });
  return res.data.token;
}

app.post('/api/pesapal/submit-order', protect, async (req, res) => {
  try {
    const token = await getPesapalToken();
    const orderData = {
      id: req.user._id.toString(),
      currency_code: 'KES',
      amount: 2500,
      description: 'Laptop Tracker Subscription',
      callback_url: 'https://laptop-tracker-2h7l.onrender.com/dashboard',
      notification_id: '',
      ordering_reference: 'LAPTOP_' + Date.now(),
      meta_data: [{ key: 'user_id', value: req.user._id.toString() }],
      items: [{ title: 'Subscription', quantity: 1, unit_cost: 2500 }]
    };
    const response = await axios.post(`${PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest`, orderData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json', Accept: 'application/json' }
    });
    res.json({ redirect_url: response.data.RedirectURL });
  } catch (err) {
    res.status(500).json({ error: 'Pesapal failed' });
  }
});
// --- END PESAPAL ---
"""

if 'PESAPAL_CONSUMER_KEY' not in server:
    server += pesapal_server_code
    with open('server.js', 'w') as f:
        f.write(server)
    print("✅ Server updated safely.")
else:
    print("⏭️ Server already has Pesapal code.")

# 2. Update subscription.html SAFELY (Only adds, never deletes)
with open('public/subscription.html', 'r') as f:
    html = f.read()

pesapal_button = '<button class="btn btn-pesapal" onclick="payPesapal()" style="background-color: #005b9f; color: white; width: 100%; padding: 15px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; margin: 15px 0; cursor: pointer;">💳 Pay with Pesapal (Card & Mobile Money)</button>'

pesapal_script = """
<script>
window.payPesapal = async () => {
  const btn = event.target;
  btn.textContent = 'Processing...';
  btn.disabled = true;
  try {
    const res = await fetch('/api/pesapal/submit-order', { method: 'POST', headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token'), 'Content-Type': 'application/json' }, body: JSON.stringify({ amount: 2500 }) });
    const data = await res.json();
    if (data.redirect_url) {
      window.location.href = data.redirect_url;
    } else {
      alert(data.error || 'Pesapal failed');
      btn.textContent = '💳 Pay with Pesapal (Card & Mobile Money)';
      btn.disabled = false;
    }
  } catch (err) {
    alert('Network error');
    btn.textContent = '💳 Pay with Pesapal (Card & Mobile Money)';
    btn.disabled = false;
  }
};
</script>
"""

if 'payPesapal' not in html:
    # Insert button BEFORE the back button (does not delete back button)
    html = html.replace('<button class="btn btn-back"', pesapal_button + '\n    <button class="btn btn-back"')
    # Insert script BEFORE </body>
    html = html.replace('</body>', pesapal_script + '\n</body>')
    with open('public/subscription.html', 'w') as f:
        f.write(html)
    print("✅ Frontend updated safely.")
else:
    print("⏭️ Frontend already has Pesapal code.")
