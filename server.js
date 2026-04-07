const express = require("express");
const mongoose = require("mongoose");
const path = require("path");

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// MongoDB connection (Render ENV)
mongoose.connect(process.env.MONGO_URI)
.then(() => console.log("✅ MongoDB Connected"))
.catch(err => console.log("❌ MongoDB Error:", err));

// ================= USER SCHEMA =================
const userSchema = new mongoose.Schema({
  email: String,
  password: String
});

const User = mongoose.model("User", userSchema);

// ================= LAPTOP SCHEMA =================
const laptopSchema = new mongoose.Schema({
  brand: String,
  model: String,
  serial: String,
  processor: String,
  ram: String,
  storage: String,
  owner: String,
  status: { type: String, default: "safe" }
});

const Laptop = mongoose.model("Laptop", laptopSchema);

// ================= ROUTES =================

// Register User
app.post("/registerUser", async (req, res) => {
  const { email, password } = req.body;

  const newUser = new User({ email, password });
  await newUser.save();

  res.send("User Registered");
});

// Login User
app.post("/login", (req, res) => {
  const email = req.body.email;
  const password = req.body.password;

  User.findOne({ email: email, password: password })
    .then(user => {
      if (user) {
        res.redirect("/dashboard.html");
      } else {
        res.send("Invalid login");
      }
    })
    .catch(err => {
      console.log(err);
      res.send("Server error");
    });
});

// Register Laptop
app.post("/registerLaptop", async (req, res) => {
  const laptop = new Laptop(req.body);
  await laptop.save();

  res.send("Laptop Registered Successfully");
});

// Get All Laptops
app.get("/laptops", async (req, res) => {
  const laptops = await Laptop.find();
  res.json(laptops);
});

// Mark as Stolen
app.post("/markStolen/:id", async (req, res) => {
  await Laptop.findByIdAndUpdate(req.params.id, { status: "stolen" });
  res.send("Marked as stolen");
});

// Delete Laptop
app.delete("/deleteLaptop/:id", async (req, res) => {
  await Laptop.findByIdAndDelete(req.params.id);
  res.send("Deleted");
});

// ================= START SERVER =================
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
