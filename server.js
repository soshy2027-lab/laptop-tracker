const express = require("express");
const mongoose = require("mongoose");

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// ✅ CONNECT TO MONGODB (STRICT + SAFE)
mongoose.connect(process.env.MONGO_URI)
.then(() => {
  console.log("✅ MongoDB Connected");
})
.catch((err) => {
  console.log("❌ MongoDB ERROR:", err.message);
});

// ✅ SCHEMA
const Laptop = mongoose.model("Laptop", {
  brand: String,
  model: String,
  serial: String
});

// ✅ SAVE LAPTOP
app.post("/add-laptop", async (req, res) => {
  try {
    const { brand, model, serial } = req.body;

    if (!brand || !model || !serial) {
      return res.status(400).send("Missing fields");
    }

    const newLaptop = new Laptop({ brand, model, serial });
    await newLaptop.save();

    res.send("saved");
  } catch (err) {
    console.log("SAVE ERROR:", err.message);
    res.status(500).send("error");
  }
});

// ✅ GET LAPTOPS
app.get("/get-laptops", async (req, res) => {
  try {
    const laptops = await Laptop.find();
    res.json(laptops);
  } catch (err) {
    console.log("FETCH ERROR:", err.message);
    res.status(500).send("error");
  }
});

// ✅ START SERVER
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Server running"));
