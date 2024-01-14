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
    message_time: new Date(),
    assistant: '',
    chat_id,
    user_message,
  };
};
