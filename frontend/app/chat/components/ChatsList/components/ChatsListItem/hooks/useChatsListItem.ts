import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from 'react-i18next'

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
  const { t } = useTranslation(['chat']);

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
        text: t('chatDeleted',{ id: chatId,ns:'chat'})  ,
        variant: "success",
      });
    } catch (error) {
      console.error(t('errorDeleting',{ error: error, ns:'chat'}));
      publish({
        text: t('errorDeleting',{ error: error, ns:'chat'}),
        variant: "danger",
      });
    }
  };

  const updateChatName = async () => {
    if (chatName !== chat.chat_name) {
      await updateChat(chat.chat_id, { chat_name: chatName });
      publish({ 
        text: t('chatNameUpdated',{ ns:'chat'}), 
        variant: "success" 
      });
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
