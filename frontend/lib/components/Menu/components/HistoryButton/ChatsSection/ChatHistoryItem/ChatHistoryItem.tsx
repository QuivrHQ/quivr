import Link from "next/link";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./ChatHistoryItem.module.scss";

import { useChatsListItem } from "../../hooks/useChatsListItem";

type ChatHistoryItemProps = {
  chatHistoryItem: ChatEntity;
};

export const ChatHistoryItem = ({
  chatHistoryItem,
}: ChatHistoryItemProps): JSX.Element => {
  const {
    chatName,
    deleteChat,
    editingName,
    handleEditNameClick,
    setChatName,
  } = useChatsListItem(chatHistoryItem);

  const onNameEdited = () => {
    handleEditNameClick();
  };

  return (
    <div className={styles.chat_item_wrapper}>
      {editingName ? (
        <input
          className={styles.edit_chat_name}
          onChange={(event) => setChatName(event.target.value)}
          value={chatName}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              onNameEdited();
            }
          }}
          autoFocus
        />
      ) : (
        <Link
          className={styles.chat_item_name}
          href={`/chat/${chatHistoryItem.chat_id}`}
        >
          {chatName.trim()}
        </Link>
      )}
      <div className={styles.icons_wrapper}>
        <Icon
          name={editingName ? "check" : "edit"}
          size="normal"
          color="black"
          handleHover={true}
          onClick={() => onNameEdited()}
        />
        <Icon
          name="delete"
          size="normal"
          color="dangerous"
          handleHover={true}
          onClick={() => void deleteChat()}
        />
      </div>
    </div>
  );
};
