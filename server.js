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
});
