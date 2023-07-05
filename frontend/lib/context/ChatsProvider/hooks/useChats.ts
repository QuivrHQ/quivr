/* eslint-disable */
import { UUID } from "crypto";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { useToast } from "@/lib/hooks/useToast";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import { useChatApi } from "@/lib/api/chat/useChatApi";

export default function useChats() {
  const [allChats, setAllChats] = useState<ChatEntity[]>([]);

  const router = useRouter();
  const { publish } = useToast();

  const { getChats, deleteChat } = useChatApi();

  const fetchAllChats = async () => {
    try {
      const response = await getChats();
      setAllChats(response.reverse());
    } catch (error) {
      console.error(error);
      publish({
        variant: "danger",
        text: "Error occurred while fetching your chats",
      });
    }
  };

  const deleteChatHandler = async (chatId: UUID) => {
    try {
      await deleteChat(chatId);
      setAllChats((chats) => chats.filter((chat) => chat.chat_id !== chatId));
      // TODO: Change route only when the current chat is being deleted
      router.push("/chat");
      publish({
        text: `Chat sucessfully deleted. Id: ${chatId}`,
        variant: "success",
      });
    } catch (error) {
      console.error("Error deleting chat:", error);
      publish({ text: `Error deleting chat: ${error}`, variant: "danger" });
    }
  };

  useEffect(() => {
    fetchAllChats();
  }, []);

  return {
    allChats,
    deleteChat: deleteChatHandler,
  };
}
