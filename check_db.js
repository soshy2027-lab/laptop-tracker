const mongoose = require('mongoose');

const MONGO_URI = 'mongodb+srv://admin:3lRFR2y22nZJR4TX@cluster0.oipocbo.mongodb.net/?appName=Cluster0';

async function checkData() {
  await mongoose.connect(MONGO_URI);
  console.log('✅ Connected to database');

  const User = mongoose.model('User', new mongoose.Schema({}, { strict: false }));
  const Laptop = mongoose.model('Laptop', new mongoose.Schema({}, { strict: false }));

  console.log('\n=== USERS ===');
  const users = await User.find({});
  console.log(`Total Users: ${users.length}`);
  users.forEach(u => {
    console.log(`- ${u.name || 'No Name'} | ${u.email || 'No Email'} | Role: ${u.role || 'user'}`);
  });

  console.log('\n=== LAPTOPS ===');
  const laptops = await Laptop.find({});
  console.log(`Total Laptops: ${laptops.length}`);
  laptops.forEach(l => {
    const ownerId = l.user || l.userId || l.owner || l.ownerId;
    console.log(`- Brand: ${l.brand || 'Unknown'} | Serial: ${l.serialNumber || l.serial || 'Unknown'} | OwnerID: ${ownerId || 'Missing!'}`);
  });

  await mongoose.disconnect();
  console.log('\n✅ Done');
}

checkData().catch(err => console.error('❌ Error:', err.message));
