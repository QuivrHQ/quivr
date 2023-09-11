import { ChatHistory } from "@/app/chat/[chatId]/types";

import { MessageRow } from "./components";

type ChatMessageProps = {
  content: ChatHistory;
};
export const ChatMessage = ({ content }: ChatMessageProps): JSX.Element => {
  const { assistant, message_id, user_message, brain_name, prompt_title } =
    content;

  return (
    <>
      <MessageRow
        key={`user-${message_id}`}
        speaker={"user"}
        text={user_message}
        promptName={prompt_title}
        brainName={brain_name}
      />
      <MessageRow
        key={`assistant-${message_id}`}
        speaker={"assistant"}
        text={assistant}
        brainName={brain_name}
        promptName={prompt_title}
      />
    </>
  );
};
