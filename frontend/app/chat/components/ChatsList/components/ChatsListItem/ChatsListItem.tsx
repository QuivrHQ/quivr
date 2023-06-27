import { UUID } from "crypto";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { FiEdit, FiSave, FiTrash2 } from "react-icons/fi";
import { MdChatBubbleOutline } from "react-icons/md";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import { useAxios, useToast } from "@/lib/hooks";
import { cn } from "@/lib/utils";

import { ChatName } from "./components/ChatName";

interface ChatsListItemProps {
  chat: ChatEntity;
  deleteChat: (id: UUID) => void;
}

export const ChatsListItem = ({
  chat,
  deleteChat,
}: ChatsListItemProps): JSX.Element => {
  const pathname = usePathname()?.split("/").at(-1);
  const selected = chat.chat_id === pathname;
  const [chatName, setChatName] = useState(chat.chat_name);
  const { axiosInstance } = useAxios();
  const { publish } = useToast();
  const [editingName, setEditingName] = useState(false);

  const updateChatName = async () => {
    if (chatName !== chat.chat_name) {
      await axiosInstance.put<ChatEntity>(`/chat/${chat.chat_id}/metadata`, {
        chat_name: chatName,
      });
      publish({ text: "Chat name updated", variant: "success" });
    }
  };

  const handleEditNameClick = () => {
    if (editingName) {
      setEditingName(false);
      void updateChatName();
    } else {
      setEditingName(true);
    }
  };

  return (
    <div
      className={cn(
        "w-full border-b border-black/10 dark:border-white/25 last:border-none relative group flex overflow-x-hidden hover:bg-gray-100 dark:hover:bg-gray-800",
        selected
          ? "bg-gray-100 dark:bg-gray-800 text-primary dark:text-white"
          : ""
      )}
    >
      <Link
        className="flex flex-col flex-1 min-w-0 p-4"
        href={`/chat/${chat.chat_id}`}
        key={chat.chat_id}
      >
        <div className="flex items-center gap-2">
          <MdChatBubbleOutline className="text-xl" />
          <ChatName
            setName={setChatName}
            editing={editingName}
            name={chatName}
          />
        </div>
        <div className="grid-cols-2 text-xs opacity-50 whitespace-nowrap">
          {chat.chat_id}
        </div>
      </Link>
      <div className="opacity-0 group-hover:opacity-100 flex items-center justify-center hover:text-red-700 bg-gradient-to-l from-white dark:from-black to-transparent z-10 transition-opacity">
        <button className="p-0" type="button" onClick={handleEditNameClick}>
          {editingName ? <FiSave /> : <FiEdit />}
        </button>
        <button
          className="p-5"
          type="button"
          onClick={() => deleteChat(chat.chat_id)}
        >
          <FiTrash2 />
        </button>
      </div>

      {/* Fade to white */}
      <div
        aria-hidden
        className="not-sr-only absolute left-1/2 top-0 bottom-0 right-0 bg-gradient-to-r from-transparent to-white dark:to-black pointer-events-none"
      ></div>
    </div>
  );
};
