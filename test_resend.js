require('dotenv').config();
const { Resend } = require('resend');
const resend = new Resend(process.env.RESEND_API_KEY);

async function test() {
  try {
    const data = await resend.emails.send({
      from: process.env.FROM_EMAIL || 'onboarding@resend.dev',
      to: process.env.ADMIN_EMAIL || 'your-email@example.com', // Replace with your real email to test
      subject: 'Test Email',
      html: '<p>This is a test from Laptop Tracker!</p>'
    });
    console.log('✅ SUCCESS:', data);
  } catch (error) {
    console.error('❌ ERROR:', error.message);
  }
}
test();
