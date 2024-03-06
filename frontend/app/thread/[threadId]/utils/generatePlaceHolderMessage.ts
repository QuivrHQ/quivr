import { ThreadMessage } from "../types";

type GeneratePlaceHolderMessageProps = {
  user_message: string;
  thread_id: string;
};

export const generatePlaceHolderMessage = ({
  user_message,
  thread_id,
}: GeneratePlaceHolderMessageProps): ThreadMessage => {
  return {
    message_id: new Date().getTime().toString(),
    message_time: new Date(
      new Date().setDate(new Date().getDate() + 1)
    ).toISOString(),
    assistant: "🧠",
    thread_id,
    user_message,
  };
};
