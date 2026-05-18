const fs = require('fs');
const bcrypt = require('bcryptjs');

const db = JSON.parse(fs.readFileSync('./data.json', 'utf8'));
const admin = db.users.find(u => u.email === 'admin@laptoptracker.com');

(async () => {
  if (admin) {
    const newPassword = 'admin232';
    admin.password = await bcrypt.hash(newPassword, 10);
    admin.role = 'admin';
    admin.isSubscribed = true;
    fs.writeFileSync('./data.json', JSON.stringify(db, null, 2));
    console.log('✅ Password reset to: admin232');
  }
})();