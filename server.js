const express = require("express");
const mongoose = require("mongoose");

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// CONNECT DB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log("DB Connected"))
.catch(err => console.log("DB ERROR:", err));

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

// REGISTER
app.post("/registerUser", async (req,res)=>{
  await new User(req.body).save();
  res.redirect("/login.html");
});

// LOGIN (NO ERROR VERSION)
app.post("/login", (req,res)=>{
  if(req.body.email && req.body.password){
    res.redirect("/dashboard.html");
  } else {
    res.send("Login failed");
  }
});

// SAVE LAPTOP
app.post("/add-laptop", async (req,res)=>{
  try{
    await new Laptop(req.body).save();
    res.send("saved");
  }catch(e){
    res.send("error");
  }
});

// GET LAPTOPS
app.get("/get-laptops", async (req, res) => {
  try {
    const data = await Laptop.find();
    res.json(data);
  } catch (err) {
    console.log("FETCH ERROR:", err);
    res.send("error");
  }
});

app.listen(process.env.PORT || 3000);
