
const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const path = require("path");

const app = express();

app.use(bodyParser.json());
app.use(express.static(__dirname));

// Connect to MongoDB Atlas
mongoose.connect("mongodb+srv://Laptopadmin:laptop12345@cluster0.xbkdoxy.mongodb.net/laptopTracker?retryWrites=true&w=majority")
.then(() => console.log("✅ Connected to MongoDB Atlas"))
.catch(err => console.error("❌ MongoDB error:", err));

// Laptop Schema
const userSchema = new mongoose.Schema({
    email: String,
    password: String
});
app.post("/registerUser", async (req, res) => {
    try {
        const { email, password } = req.body;

        const user = new User({ email, password });
        await user.save();

        res.json({ message: "User registered" });

    } catch (err) {
        res.status(500).json({ message: "Error registering user" });
    }

});
app.post("/loginUser", async (req, res) => {
    try {
        const { email, password } = req.body;

        const user = await User.findOne({ email, password });

        if (!user) {
            return res.json({ success: false, message: "Invalid login" });
        }

        res.json({ success: true });

    } catch (err) {
        res.status(500).json({ message: "Login error" });
    }
});
app.post("/updateLaptop", async (req, res) => {
    try {
        const { id, brand, model, serial, processor, ram, storage } = req.body;

        await Laptop.findByIdAndUpdate(id, {
            brand,
            model,
            serial,
            processor,
            ram,
            storage
        });

        res.json({ message: "Updated" });

    } catch (err) {
        res.status(500).json({ message: "Update error" });
    }
});

const User = mongoose.model("User", userSchema);
const laptopSchema = new mongoose.Schema({
    brand: String,
    model: String,
    serial: String,
    processor: String,
    ram: String,
    storage: String,
    owner: String, // NEW FIELD
    status: { type: String, default: "safe" }
});

const Laptop = mongoose.model("Laptop", laptopSchema);

// Register Laptop
app.post("/registerLaptop", async (req, res) => {
    try {
        const { brand, model, serial, processor, ram, storage, owner } = req.body;

        const laptop = new Laptop({
            brand,
            model,
            serial,
            processor,
            ram,
            storage,
            owner
        });

        await laptop.save();

        res.json({ message: "Laptop saved successfully" });

    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Error saving laptop" });
    }
});

// Get All Laptops
app.get("/allLaptops", async (req, res) => {
    const laptops = await Laptop.find();
    res.json(laptops);
});

// Mark as Stolen
app.post("/markStolen", async (req, res) => {
    const { serial } = req.body;
    await Laptop.updateOne({ serial: serial }, { status: "stolen" });
    res.json({ message: "Marked as stolen" });
});

// Start Server
app.listen(3000, () => {
    console.log("Server running at http://localhost:3000");
=======
// server.js
const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// ✅ To parse form data
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// ✅ Serve static files from public folder
app.use(express.static('public'));

// ✅ Test route
app.get('/test', (req, res) => {
    res.json({ message: "Server is working ✅" });
});

// ✅ Route to handle form submission (for now just console log)
app.post('/submit-laptop', (req, res) => {
    console.log('Form data received:', req.body);
    // For now, just send a success message
    res.send('Laptop details submitted successfully!');
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
>>>>>>> 1bcbd0cf4329a5b488d382e1f4ff6c239d26fe8d
});
