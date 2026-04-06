const { createClient } = require("@supabase/supabase-js");

<<<<<<< HEAD
const supabaseUrl = "YOUR_URL";
const supabaseKey = "YOUR_ANON_KEY";

const supabase = createClient(supabaseUrl, supabaseKey);

async function testConnection() {
    const { data, error } = await supabase
        .from("laptops")
        .select("*")
        .limit(1);

    if (error) {
        console.log("❌ Supabase Error:", error.message);
    } else {
        console.log("✅ Supabase Connected!");
=======
const SUPABASE_URL = "https://ytalqhmarprgojenbbsn.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0YWxxaG1hcnByZ29qZW5iYnNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ2NjA0NDksImV4cCI6MjA4MDIzNjQ0OX0.Qr5noF-HkXo_VHd4gTr_PYUFeJUm8oFFQLdroRxtxdk";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function testConnection() {
    const { data, error } = await supabase.from("test").select("*");

    if (error) {
        console.log("❌ Supabase connection FAILED");
        console.log(error.message);
    } else {
        console.log("✅ Supabase connection SUCCESS!");
>>>>>>> 1bcbd0cf4329a5b488d382e1f4ff6c239d26fe8d
        console.log(data);
    }
}

<<<<<<< HEAD
testConnection();;
=======
testConnection();
>>>>>>> 1bcbd0cf4329a5b488d382e1f4ff6c239d26fe8d
