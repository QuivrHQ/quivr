import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import Icon from "@/lib/components/ui/Icon/Icon";
import { OptionsModal } from "@/lib/components/ui/OptionsModal/OptionsModal";
import { Option } from "@/lib/types/Options";

import styles from "./ThreadItem.module.scss";

import { useChatsListItem } from "../../hooks/useChatsListItem";

type ChatHistoryItemProps = {
  chatHistoryItem: ChatEntity;
};

export const ThreadItem = ({
  chatHistoryItem,
}: ChatHistoryItemProps): JSX.Element => {
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);

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

  const optionsRef = useRef<HTMLDivElement | null>(null);
  const iconRef = useRef<HTMLDivElement | null>(null);

  const options: Option[] = [
    {
      label: "Edit",
      onClick: () => onNameEdited(),
      iconName: "edit",
      iconColor: "primary",
    },
    {
      label: "Delete",
      onClick: () => void deleteChat(),
      iconName: "delete",
      iconColor: "dangerous",
    },
  ];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        iconRef.current &&
        !iconRef.current.contains(event.target as Node) &&
        optionsRef.current &&
        !optionsRef.current.contains(event.target as Node)
      ) {
        setOptionsOpened(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <>
      <div className={styles.thread_item_wrapper}>
        {editingName ? (
          <input
            className={styles.edit_thread_name}
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
            className={styles.thread_item_name}
            href={`/chat/${chatHistoryItem.chat_id}`}
          >
            {chatName.trim()}
          </Link>
        )}
        <div
          ref={iconRef}
          onClick={(event: React.MouseEvent<HTMLElement>) => {
            event.nativeEvent.stopImmediatePropagation();
            if (editingName) {
              onNameEdited();
            } else {
              setOptionsOpened(!optionsOpened);
            }
          }}
        >
          <Icon
            name={editingName ? "check" : "options"}
            size="small"
            color="black"
            handleHover={true}
          />
          <div ref={optionsRef} className={styles.options_modal}>
            {optionsOpened && <OptionsModal options={options} />}
          </div>
        </div>
      </div>
    </>
  );
};
