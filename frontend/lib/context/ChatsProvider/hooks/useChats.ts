/* eslint-disable */
import { UUID } from "crypto";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { useAxios } from "@/lib/hooks";
import { useToast } from "@/lib/hooks/useToast";

import { ChatEntity } from "@/app/chat/[chatId]/types";

export default function useChats() {
  const [allChats, setAllChats] = useState<ChatEntity[]>([]);

  const { axiosInstance } = useAxios();

  const router = useRouter();
  const { publish } = useToast();

  const fetchAllChats = async () => {
    try {
      console.log("Fetching all chats");
      const response = await axiosInstance.get<{
        chats: ChatEntity[];
      }>(`/chat`);
      setAllChats(response.data.chats.reverse());
      console.log("Fetched all chats");
    } catch (error) {
      console.error(error);
      publish({
        variant: "danger",
        text: "Error occured while fetching your chats",
      });
    }
  };

  const deleteChat = async (chatId: UUID) => {
    try {
      await axiosInstance.delete(`/chat/${chatId}`);
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
    deleteChat,
  };
}
