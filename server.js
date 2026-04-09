const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const path = require("path");

const app = express();

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// MongoDB Connection (Render ENV)
mongoose.connect(process.env.MONGO_URI)
.then(() => console.log("✅ MongoDB Connected"))
.catch(err => console.log("❌ MongoDB Error:", err));

// ================= USER =================
const userSchema = new mongoose.Schema({
  email: String,
  password: String
});

const User = mongoose.model("User", userSchema);

// Register
app.post("/registerUser", async (req, res) => {
  try {
    const user = new User(req.body);
    await user.save();
    res.redirect("/login.html");
  } catch (err) {
    res.send("Error registering user");
  }
});

// Login (simple)
app.post("/login", async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email, password });

  if (user) {
    res.redirect("/dashboard.html");
  } else {
    res.send("Invalid login");
  }
});

// ================= LAPTOP =================
const laptopSchema = new mongoose.Schema({
  brand: String,
  model: String,
  serial: String,
  processor: String,
  ram: String,
  storage: String
});

const Laptop = mongoose.model("Laptop", laptopSchema);

// Save Laptop
app.post("/add-laptop", async (req, res) => {
  try {
    const laptop = new Laptop(req.body);
    await laptop.save();
    res.redirect("/dashboard.html");
  } catch (err) {
    console.log(err);
    res.send("Error saving laptop");
  }
});

// Get Laptops (for display later)
app.get("/get-laptops", async (req, res) => {
  try {
    const laptops = await Laptop.find();
    res.json(laptops);
  } catch (err) {
    console.log(err);
    res.json([]);
  }
});

// ================= SERVER =================
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
