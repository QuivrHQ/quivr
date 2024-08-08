import { ChatMessage } from "@/app/chat/[chatId]/types";

import { MessageRow } from "./components/MessageRow/MessageRow";
import "./styles.css";

type QADisplayProps = {
  content: ChatMessage;
  index: number;
  lastMessage?: boolean;
};
export const QADisplay = ({
  content,
  index,
  lastMessage,
}: QADisplayProps): JSX.Element => {
  const { assistant, message_id, user_message, brain_name, metadata, thumbs } =
    content;

  return (
    <>
      <MessageRow
        key={`user-${message_id}`}
        speaker={"user"}
        text={user_message}
        metadata={metadata}
      />
      <MessageRow
        key={`assistant-${message_id}`}
        speaker={"assistant"}
        text={assistant}
        brainName={brain_name ?? metadata?.metadata_model?.display_name}
        index={index}
        metadata={metadata}
        messageId={message_id}
        thumbs={thumbs}
        lastMessage={lastMessage}
      />
    </>
  );
};
