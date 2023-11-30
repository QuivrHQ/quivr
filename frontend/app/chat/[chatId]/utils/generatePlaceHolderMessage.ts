import { ChatMessage } from "../types";

type GeneratePlaceHolderMessageProps = {
  user_message: string;
  chat_id: string;
};

export const generatePlaceHolderMessage = ({
  user_message,
  chat_id,
}: GeneratePlaceHolderMessageProps): ChatMessage => {
  const message_id = new Date().getTime().toString();
  const message_time = new Date().toISOString();
  const assistant = "";

  return {
    message_id,
    message_time,
    assistant,
    chat_id,
    user_message,
  };
};
