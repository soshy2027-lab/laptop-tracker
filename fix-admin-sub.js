const fs = require('fs');
const DB_FILE = './data.json';
const db = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));

const adminUser = db.users.find(u => u.email === 'admin@laptoptracker.com');

if (adminUser) {
  adminUser.role = 'admin';
  adminUser.isSubscribed = true;
  adminUser.subscriptionExpiryDate = new Date('2099-12-31').toISOString();
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
  console.log('✅ Admin subscription fixed!');
} else {
  console.log('❌ Admin not found');
}