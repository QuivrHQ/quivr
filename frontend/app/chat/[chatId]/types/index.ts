export type ChatQuestion = {
  model: string;
  question?: string;
  temperature: number;
  max_tokens: number;
};
export type ChatHistory = {
  chat_id: string;
  message_id: string;
  user_message: string;
  assistant: string;
  message_time: string;
};
