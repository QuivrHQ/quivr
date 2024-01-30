import { ChatEntity } from "@/app/chat/[chatId]/types";

import { ChatHistoryItem } from "./ChatHistoryItem/ChatHistoryItem";
import styles from "./ChatsSection.module.scss";

type ChatSectionProps = {
  chats: ChatEntity[];
  title: string;
};

export const ChatsSection = (props: ChatSectionProps): JSX.Element => {
  if (props.chats.length === 0) {
    return <></>;
  }

  return (
    <div>
      <div>{props.title}</div>
      <div className={styles.chats_wrapper}>
        {props.chats.map((chat) => (
          <ChatHistoryItem key={chat.chat_id} chatHistoryItem={chat} />
        ))}
      </div>
    </div>
  );
};
