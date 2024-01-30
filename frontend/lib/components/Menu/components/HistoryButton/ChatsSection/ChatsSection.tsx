import Link from "next/link";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import Icon from "@/lib/components/ui/Icon/Icon";

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
            className={styles.chat_item_wrapper}
            href={`/chat/${chat.chat_id}`}
            key={chat.chat_id}
          >
            <div className={styles.chat_item_name}>{chat.chat_name.trim()}</div>
            <div className={styles.icons_wrapper}>
              <Icon
                name="edit"
                size="normal"
                color="white"
                handleHover={true}
              />
              <Icon
                name="delete"
                size="normal"
                color="white"
                handleHover={true}
              />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};
