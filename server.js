const express = require("express");
const mongoose = require("mongoose");

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// MongoDB
mongoose.connect(process.env.MONGO_URI)
.then(()=>console.log("DB Connected"))
.catch(err=>console.log(err));

// USER
const User = mongoose.model("User", {
  email: String,
  password: String
});

// LAPTOP
const Laptop = mongoose.model("Laptop", {
  brand: String,
  model: String,
  serial: String
});

// Register
app.post("/registerUser", async (req,res)=>{
  await new User(req.body).save();
  res.redirect("/login.html");
});

// Login
app.post("/login", async (req,res)=>{
  const user = await User.findOne(req.body);
  if(user) res.redirect("/dashboard.html");
  else res.send("Invalid");
});

// Save Laptop
app.post("/add-laptop", async (req, res) => {
  try {
    console.log("DATA:", req.body);

    const laptop = new Laptop({
      brand: req.body.brand,
      model: req.body.model,
      serial: req.body.serial
    });

    await laptop.save();

    res.send("saved");
  } catch (err) {
    console.log("ERROR:", err);
    res.send("error");
  }
});

// Get Laptops
app.get("/get-laptops", async (req,res)=>{
  const data = await Laptop.find();
  res.json(data);
});

// Start
app.listen(process.env.PORT || 3000);
