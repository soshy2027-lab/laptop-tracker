const express = require("express");
const mongoose = require("mongoose");

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

/* ===== DATABASE ===== */
mongoose.connect(process.env.MONGO_URI)
.then(() => console.log("MongoDB Connected"))
.catch(err => console.log("DB Error:", err.message));

/* ===== MODELS ===== */
const User = mongoose.model("User", {
  email: String,
  password: String
});

const Laptop = mongoose.model("Laptop", {
  brand: String,
  model: String,
  serial: String
});

/* ===== ROUTES ===== */

// REGISTER
app.post("/registerUser", async (req, res) => {
  try {
    await new User(req.body).save();
    res.redirect("/login.html");
  } catch (err) {
    res.send("error");
  }
});

// LOGIN (IMPORTANT FIX)
app.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });

    if (!user) return res.send("User not found");

    if (user.password !== password) return res.send("Wrong password");

    res.redirect("/dashboard.html");

  } catch (err) {
    console.log(err);
    res.send("error");
  }
});

// SAVE LAPTOP
app.post("/add-laptop", async (req, res) => {
  try {
    await new Laptop(req.body).save();
    res.send("saved");
  } catch (err) {
    res.send("error");
  }
});

// GET LAPTOPS
app.get("/get-laptops", async (req, res) => {
  try {
    const data = await Laptop.find();
    res.json(data);
  } catch (err) {
    res.send("error");
  }
});

/* ===== START SERVER ===== */
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Server running"));
