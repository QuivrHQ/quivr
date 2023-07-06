/* Instructions:
1. in .backend/supabase folder, create .env file with BEEHIIV_PUBLICATION_ID and BEEHIIV_API_KEY variables
2. cd into .backend
--- for the rest of these steps you will need your supabase project id which can be found in your console url: https://supabase.com/dashboard/project/<projectId> ---
3. run `supabase secrets set --env-file ./supabase/.env` to set the environment variables
4. run `supabase functions deploy add-new-email` to deploy the function
5. in the supabase console go to Database/Webhook and create new and point it to the edge function 'add-new-email'. You will have to add a new header Authorization: Bearer ${anon public key from Settings/API} to the webhook.
*/

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const publicationId = Deno.env.get("BEEHIIV_PUBLICATION_ID");
const apiKey = Deno.env.get("BEEHIIV_API_KEY");

const url = `https://api.beehiiv.com/v2/publications/${publicationId}/subscriptions`;

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

serve(
  async (req: { json: () => WebhookPayload | PromiseLike<WebhookPayload> }) => {
    if (!publicationId || !apiKey) {
      throw new Error("Missing required environment variables");
    }

    const payload: WebhookPayload = await req.json();

    if (payload.record.email) {
      const requestBody = {
        email: payload.record.email,
        send_welcome_email: false,
        utm_source: "quivr",
        utm_medium: "organic",
        referring_site: "https://quivr.app",
      };

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
          Accept: "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(
          `Error adding email to Beehiiv: ${JSON.stringify(response)}`
        );
      }

      const responseBody = await response.json();
      return new Response(JSON.stringify(responseBody), {
        status: response.status,
        headers: { "Content-Type": "application/json" },
      });
    }

    throw new Error(
      `No email address found in payload: ${JSON.stringify(payload)}`
    );
  }
);
