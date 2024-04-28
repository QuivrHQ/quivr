/* Instructions:

--- for the rest of these steps you will need your supabase project id which can be found in your console url: https://supabase.com/dashboard/project/<projectId> ---
3. run `supabase secrets set --env-file ./supabase/.env` to set the environment variables
4. run `supabase functions deploy add-new-email` to deploy the function
5. in the supabase console go to Database/Webhook and create new and point it to the edge function 'add-new-email'. You will have to add a new header Authorization: Bearer ${anon public key from Settings/API} to the webhook.
*/

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const postHogApiKey = Deno.env.get("POSTHOG_API_KEY");

interface WebhookPayload {
  type: "INSERT" | "UPDATE" | "DELETE";
  table: string;
  record: {
    id: string;
    aud: string;
    role: string;
    email: string;
    phone: null;
    created_at: string;
  };
}

const postHogUrl = "https://app.posthog.com/capture/";

serve(
  async (req: { json: () => WebhookPayload | PromiseLike<WebhookPayload> }) => {
    if (!postHogApiKey) {
      throw new Error("Missing PostHog API key");
    }

    const payload: WebhookPayload = await req.json();

    if (payload.record.email && payload.type === "INSERT") {
      const postHogPayload = {
        event: "USER_SIGNED_UP",
        api_key: postHogApiKey,
        distinct_id: payload.record.id,
        properties: {
          email: payload.record.email,
        },
        timestamp: payload.record.created_at, // assuming this is in ISO 8601 format
      };

      const response = await fetch(postHogUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postHogPayload),
      });

      if (!response.ok) {
        throw new Error(
          `Error sending event to PostHog: ${response.statusText}`
        );
      }

      return new Response(null, { status: 200 });
    }

    return new Response("No new user signup event detected", { status: 200 });
  }
);
