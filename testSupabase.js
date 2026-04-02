const { createClient } = require("@supabase/supabase-js");

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
        console.log(data);
    }
}

testConnection();;
