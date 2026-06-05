with open('public/index.html', 'r') as f:
    html = f.read()

# 1. Remove the old broken code we added earlier
start_marker = "<style>\n  .auth-form { display: none;"
end_marker = "</script>\n"

start_idx = html.find(start_marker)
if start_idx != -1:
    end_idx = html.find("</script>", start_idx)
    if end_idx != -1:
        end_idx += len("</script>")
        html = html[:start_idx] + html[end_idx:]

# 2. Prepare the new code that will sit INSIDE the login box
new_html_block = '''
<div id="auth-extras" style="margin-top: 15px; text-align: center;">
    <button id="show-forgot-btn" class="link-btn" style="background: none; border: none; color: #2563eb; cursor: pointer; text-decoration: underline; font-size: 14px; padding: 0; display: none;">Forgot Password?</button>
    <div id="forgot-form" class="auth-form" style="display: none; margin-top: 15px;">
        <p style="font-size: 14px; margin-bottom: 10px;">Enter your email to receive a reset link.</p>
        <input type="email" id="forgot-email" placeholder="Enter your email" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;">
        <button onclick="handleForgot()" class="btn-primary" style="width: 100%;">Send Reset Link</button>
        <p id="forgot-msg" style="margin-top: 10px; font-size: 14px;"></p>
        <button class="link-btn" onclick="showLogin()" style="background: none; border: none; color: #2563eb; cursor: pointer; text-decoration: underline; font-size: 14px; margin-top: 10px;">Back to Login</button>
    </div>
    <div id="reset-form" class="auth-form" style="display: none; margin-top: 15px;">
        <p style="font-size: 14px; margin-bottom: 10px;">Enter your new password.</p>
        <input type="password" id="new-password" placeholder="New Password" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;">
        <button onclick="handleReset()" class="btn-primary" style="width: 100%;">Update Password</button>
        <p id="reset-msg" style="margin-top: 10px; font-size: 14px;"></p>
    </div>
</div>
<script>
  const urlParams = new URLSearchParams(window.location.search);
  const resetToken = urlParams.get('token');

  if (resetToken) {
    document.getElementById('reset-form').style.display = 'block';
    document.getElementById('show-forgot-btn').style.display = 'none';
  } else {
    if(!localStorage.getItem('token')) {
       document.getElementById('show-forgot-btn').style.display = 'inline-block';
    }
  }

  document.getElementById('show-forgot-btn').addEventListener('click', () => {
    document.getElementById('forgot-form').style.display = 'block';
    document.getElementById('show-forgot-btn').style.display = 'none';
  });

  function showLogin() {
    document.getElementById('forgot-form').style.display = 'none';
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
'''

# 3. Inject it right after the main Login button
login_btn = '<button class="btn-primary" onclick="handleLogin()">Login</button>'
html = html.replace(login_btn, login_btn + new_html_block)

with open('public/index.html', 'w') as f:
    f.write(html)
print("Layout fixed perfectly!")
