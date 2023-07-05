import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatsListItem = (chat: ChatEntity) => {
  const pathname = usePathname()?.split("/").at(-1);
  const selected = chat.chat_id === pathname;
  const [chatName, setChatName] = useState(chat.chat_name);
  const { publish } = useToast();
  const [editingName, setEditingName] = useState(false);
  const { updateChat, deleteChat } = useChatApi();
  const { setAllChats } = useChatsContext();
  const router = useRouter();

  const deleteChatHandler = async () => {
    const chatId = chat.chat_id;
    try {
      await deleteChat(chatId);
      setAllChats((chats) =>
        chats.filter((currentChat) => currentChat.chat_id !== chatId)
      );
      // TODO: Change route only when the current chat is being deleted
      void router.push("/chat");
      publish({
        text: `Chat sucessfully deleted. Id: ${chatId}`,
        variant: "success",
      });
    } catch (error) {
      console.error("Error deleting chat:", error);
      publish({
        text: `Error deleting chat: ${JSON.stringify(error)}`,
        variant: "danger",
      });
    }
  };

  const updateChatName = async () => {
    if (chatName !== chat.chat_name) {
      await updateChat(chat.chat_id, { chat_name: chatName });
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

  return {
    setChatName,
    editingName,
    chatName,
    selected,
    handleEditNameClick,
    deleteChat: deleteChatHandler,
  };
};
