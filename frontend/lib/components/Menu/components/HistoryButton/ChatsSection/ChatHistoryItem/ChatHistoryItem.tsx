import Link from "next/link";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./ChatHistoryItem.module.scss";

type ChatHistoryItemProps = {
  chatHistoryItem: ChatEntity;
};

export const ChatHistoryItem = ({
  chatHistoryItem,
}: ChatHistoryItemProps): JSX.Element => {
  return (
    <div className={styles.chat_item_wrapper}>
      <Link
        className={styles.chat_item_name}
        href={`/chat/${chatHistoryItem.chat_id}`}
      >
        {chatHistoryItem.chat_name.trim()}
      </Link>
      <div className={styles.icons_wrapper}>
        <Icon name="edit" size="normal" color="white" handleHover={true} />
        <Icon name="delete" size="normal" color="white" handleHover={true} />
      </div>
    </div>
  );
};
