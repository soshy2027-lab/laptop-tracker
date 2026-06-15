require('dotenv').config();
const mongoose = require('mongoose');

async function check() {
  await mongoose.connect(process.env.MONGODB_URI);
  const Laptop = mongoose.model('Laptop', new mongoose.Schema({}, { strict: false }));
  const laptops = await Laptop.find({});
  console.log('Total laptops in database:', laptops.length);
  laptops.forEach(l => console.log('User:', l.user, '| Brand:', l.brand, '| Serial:', l.serial));
  process.exit(0);
}
check();
