import Link from "next/link";

import { ChatEntity } from "@/app/chat/[chatId]/types";

import styles from "./ChatsSection.module.scss";

type ChatSectionProps = {
  chats: ChatEntity[]; // replace ChatType with the actual type of your chats
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
          <Link
            className={styles.link}
            href={`/chat/${chat.chat_id}`}
            key={chat.chat_id}
          >
            <div>{chat.chat_name.trim()}</div>
          </Link>
        ))}
      </div>
    </div>
  );
};
