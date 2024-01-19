import { ChatMessage } from "@/app/chat/[chatId]/types";

import { MessageRow } from "./components";
import "./styles.css";

type QADisplayProps = {
  content: ChatMessage;
};
export const QADisplay = ({ content }: QADisplayProps): JSX.Element => {
  const {
    assistant,
    message_id,
    user_message,
    brain_name,
    prompt_title,
    metadata,
  } = content;

  return (
    <>
      <MessageRow
        key={`user-${message_id}`}
        speaker={"user"}
        text={user_message}
        promptName={prompt_title}
        brainName={brain_name}
        metadata={metadata} // eslint-disable-line @typescript-eslint/no-unsafe-assignment
      />
      <MessageRow
        key={`assistant-${message_id}`}
        speaker={"assistant"}
        text={assistant}
        brainName={brain_name}
        promptName={prompt_title}
        metadata={metadata} // eslint-disable-line @typescript-eslint/no-unsafe-assignment
      />
    </>
  );
};
