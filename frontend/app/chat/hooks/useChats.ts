import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useToast } from "@/lib/hooks/useToast";
import { useAxios } from "@/lib/useAxios";
import { UUID } from "crypto";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Chat, ChatMessage } from "../types";

export default function useChats() {
  const [allChats, setAllChats] = useState<Chat[]>([]);
  const [chat, setChat] = useState<Chat | null>(null);
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [message, setMessage] = useState<ChatMessage>(["", ""]); // for optimistic updates

  const { axiosInstance } = useAxios();
  const {
    config: { maxTokens, model, temperature },
  } = useBrainConfig();
  const router = useRouter();
  const { publish } = useToast();

  const fetchAllChats = async () => {
    const response = await axiosInstance.get<{
      chats: Chat[];
    }>(`/chat`);
    setAllChats(response.data.chats);
  };

  const fetchChat = async (chatId: UUID) => {
    const response = await axiosInstance.get<Chat>(`/chat/${chatId}`);
    setChat(response.data);
  };

  const sendMessage = async (chatId?: UUID, msg?: ChatMessage) => {
    setIsSendingMessage(true);

    if (msg) setMessage(msg);

    const response = await axiosInstance.post<Chat>(`/chat`, {
      ...(chatId && { chat_id: chatId }),
      model,
      question: msg ? msg[1] : message[1],
      history,
      temperature,
      max_tokens: maxTokens,
    });
    setChat(response.data);
    setMessage(["", ""]);
    setIsSendingMessage(false);
  };

  const deleteChat = async (chatId: UUID) => {
    try {
      await axiosInstance.delete(`/chat/${chatId}`);
      setAllChats((chats) => chats.filter((chat) => chat.chatId !== chatId));
      //DOES NOT WORK
      // check if the current chat is the one being deleted
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
  return {
    allChats,
    chat,
    isSendingMessage,
    message,
    setMessage,

    fetchAllChats,
    fetchChat,

    deleteChat,
    sendMessage,
  };
}
