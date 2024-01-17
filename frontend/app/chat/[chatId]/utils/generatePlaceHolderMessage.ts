import { ChatMessage } from "../types";

type GeneratePlaceHolderMessageProps = {
  user_message: string;
  chat_id: string;
};

export const generatePlaceHolderMessage = ({
  user_message,
  chat_id,
}: GeneratePlaceHolderMessageProps): ChatMessage => {
  return {
    message_id: new Date().getTime().toString(),
    message_time: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
    assistant: 'Thinking..',
    chat_id,
    user_message,
  };
};
