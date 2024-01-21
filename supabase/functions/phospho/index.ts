// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const phosphoApiKey = Deno.env.get("PHOSPHO_API_KEY");
const phosphoProjectKey = Deno.env.get("PHOSPHO_PROJECT_KEY");
const phosphoUrl = `https://api.phospho.ai/v2/log/${phosphoProjectKey}`;

interface ChatHistoryPayload {
  type: "UPDATE";
  table: string;
  record: {
    message_id: string;
    chat_id: string;
    user_message: string;
    assistant: string;
    message_time: string;
    // other fields as necessary
  };
}

serve(
  async (req: {
    json: () => ChatHistoryPayload | PromiseLike<ChatHistoryPayload>;
  }) => {
    if (!phosphoApiKey) {
      throw new Error("Missing Phospho API key");
    }

    const payload: ChatHistoryPayload = await req.json();

    if (payload.record.user_message && payload.type === "UPDATE") {
      const phosphoPayload = {
        batched_log_events: [
          {
            task_id: payload.record.message_id,
            session_id: payload.record.chat_id,
            input: payload.record.user_message,
            output: payload.record.assistant,
          },
        ],
      };

      const response = await fetch(phosphoUrl, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${phosphoApiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(phosphoPayload),
      });

      if (!response.ok) {
        throw new Error(
          `Error sending chat data to Phospho: ${response.statusText}`
        );
      }

      return new Response(null, { status: 200 });
    }

    return new Response("No new chat message detected", { status: 200 });
  }
);

// Remember to replace 'your_phospho_project_id' with your actual Phospho project ID.
