import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  console.log("Received request");

  const authHeader = req.headers.get("Authorization")!;
  const supabaseClient = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_ANON_KEY") ?? "",
    { global: { headers: { Authorization: authHeader } } }
  );

  // Parse the request body to get event data and the anonymous identifier
  const { anonymous_identifier, event_name, event_data } = await req.json();

  console.log(
    `Parsed request body: ${JSON.stringify({
      anonymous_identifier,
      event_name,
      event_data,
    })}`
  );

  // Insert the telemetry data along with the anonymous identifier into the Supabase table
  const { data, error } = await supabaseClient
    .from("telemetry")
    .insert([{ anonymous_identifier, event_name, event_data }]);

  if (error) {
    console.error(`Error inserting data into Supabase: ${error.message}`);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  console.log("Successfully inserted data into Supabase");
  return new Response(JSON.stringify({ message: "Telemetry logged", data }), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
    },
  });
});
