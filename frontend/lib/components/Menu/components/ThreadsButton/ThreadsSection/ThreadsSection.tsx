import { ChatEntity } from "@/app/chat/[chatId]/types";

import { ThreadItem } from "./ThreadItem/ThreadItem";
import styles from "./ThreadsSection.module.scss";

type ChatSectionProps = {
  chats: ChatEntity[];
  title: string;
};

export const ThreadsSection = (props: ChatSectionProps): JSX.Element => {
  if (props.chats.length === 0) {
    return <></>;
  }

  return (
    <div>
      <div>{props.title}</div>
      <div className={styles.chats_wrapper}>
        {props.chats.map((chat) => (
          <ThreadItem key={chat.chat_id} chatHistoryItem={chat} />
        ))}
      </div>
    </div>
  );
};
