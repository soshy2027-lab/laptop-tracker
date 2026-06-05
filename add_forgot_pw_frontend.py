with open('public/index.html', 'r') as f:
    html = f.read()

frontend_code = """
<style>
  .auth-form { display: none; margin-top: 20px; padding: 15px; background: #f9fafb; border-radius: 8px; text-align: left; }
  .auth-form.active { display: block; }
  .auth-form input { display: block; width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
  .auth-form button { padding: 10px 20px; background: #2563eb; color: white; border: none; border-radius: 5px; cursor: pointer; width: 100%; }
  .link-btn { background: none; border: none; color: #2563eb; cursor: pointer; text-decoration: underline; font-size: 14px; padding: 0; margin-top: 10px; }
  #auth-extras { max-width: 400px; margin: 20px auto; padding: 10px; text-align: center; }
</style>

<div id="auth-extras">
  <button id="show-forgot-btn" class="link-btn" style="display:none;">Forgot Password?</button>

  <div id="forgot-form" class="auth-form">
    <h3>Reset Password</h3>
    <p>Enter your email to receive a reset link.</p>
    <input type="email" id="forgot-email" placeholder="Enter your email" required>
    <button onclick="handleForgot()">Send Reset Link</button>
    <p id="forgot-msg" style="margin-top:10px; color:green;"></p>
    <button class="link-btn" onclick="showLogin()">Back to Login</button>
  </div>

  <div id="reset-form" class="auth-form">
    <h3>Enter New Password</h3>
    <input type="password" id="new-password" placeholder="New Password" required>
    <button onclick="handleReset()">Update Password</button>
    <p id="reset-msg" style="margin-top:10px; color:green;"></p>
  </div>
</div>

<script>
  const urlParams = new URLSearchParams(window.location.search);
  const resetToken = urlParams.get('token');

  if (resetToken) {
    document.getElementById('reset-form').classList.add('active');
    document.getElementById('show-forgot-btn').style.display = 'none';
  } else {
    if(!localStorage.getItem('token')) {
       document.getElementById('show-forgot-btn').style.display = 'inline-block';
    }
  }

  document.getElementById('show-forgot-btn').addEventListener('click', () => {
    document.getElementById('forgot-form').classList.add('active');
    document.getElementById('show-forgot-btn').style.display = 'none';
  });

  function showLogin() {
    document.getElementById('forgot-form').classList.remove('active');
    document.getElementById('show-forgot-btn').style.display = 'inline-block';
  }

  async function handleForgot() {
    const email = document.getElementById('forgot-email').value;
    const msg = document.getElementById('forgot-msg');
    msg.innerText = 'Sending...';
    try {
      const res = await fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const data = await res.json();
      msg.innerText = data.message || data.error;
      msg.style.color = res.ok ? 'green' : 'red';
    } catch (e) {
      msg.innerText = 'Network error';
      msg.style.color = 'red';
    }
  }

  async function handleReset() {
    const newPassword = document.getElementById('new-password').value;
    const msg = document.getElementById('reset-msg');
    msg.innerText = 'Updating...';
    try {
      const res = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: resetToken, newPassword })
      });
      const data = await res.json();
      msg.innerText = data.message || data.error;
      msg.style.color = res.ok ? 'green' : 'red';
      if(res.ok) setTimeout(() => window.location.href = '/', 2000);
    } catch (e) {
      msg.innerText = 'Network error';
      msg.style.color = 'red';
    }
  }
</script>
"""

if '</body>' in html:
    html = html.replace('</body>', frontend_code + '\n</body>')
    with open('public/index.html', 'w') as f:
        f.write(html)
    print("Frontend code added successfully!")
else:
    print("Error: Could not find </body> tag in index.html")
