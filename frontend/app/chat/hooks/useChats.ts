import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useToast } from "@/lib/hooks/useToast";
import { useAxios } from "@/lib/useAxios";
import { UUID } from "crypto";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { Chat, ChatMessage } from "../types";

export default function useChats(chatId?: UUID) {
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

  const fetchAllChats = useCallback(async () => {
    try {
      console.log("Fetching all chats");
      const response = await axiosInstance.get<{
        chats: Chat[];
      }>(`/chat`);
      setAllChats(response.data.chats);
      console.log("Fetched all chats");
    } catch (error) {
      console.error(error);
      publish({
        variant: "danger",
        text: "Error occured while fetching your chats",
      });
    }
  }, []);

  const fetchChat = useCallback(async (chatId?: UUID) => {
    if (!chatId) return;
    try {
      console.log(`Fetching chat ${chatId}`);
      const response = await axiosInstance.get<Chat>(`/chat/${chatId}`);
      console.log(response.data);

      setChat(response.data);
    } catch (error) {
      console.error(error);
      publish({
        variant: "danger",
        text: `Error occured while fetching ${chatId}`,
      });
    }
  }, []);

  type ChatResponse = Omit<Chat, "chatId"> & { chatId: UUID | undefined };

  const createChat = ({
    options,
  }: {
    options: Record<string, string | unknown>;
  }) => {
    return axiosInstance.post<ChatResponse>(`/chat`, options);
  };

  const updateChat = ({
    options,
  }: {
    options: Record<string, string | unknown>;
  }) => {
    return axiosInstance.put<ChatResponse>(`/chat/${options.chat_id}`, options);
  };

  const sendMessage = async (chatId?: UUID, msg?: ChatMessage) => {
    setIsSendingMessage(true);

    // const chat_id = {
    //   ...((chatId || currentChatId) && {
    //     chat_id: chatId ?? currentChatId,
    //   }),
    // };

    if (msg) setMessage(msg);
    const options: Record<string, unknown> = {
      // ...(chat_id && { chat_id }),
      // chat_id gets set only if either chatId or currentChatId exists, by the priority of chatId
      chat_id: chatId,
      model,
      question: msg ? msg[1] : message[1],
      history: chat ? chat.history : [],
      temperature,
      max_tokens: maxTokens,
      use_summarization: false,
    };

    const response = await (chatId !== undefined
      ? updateChat({ options })
      : createChat({ options }));

    // response.data.chatId can be undefined when the max number of requests has reached
    if (!response.data.chatId) {
      publish({
        text: "You have reached max number of requests.",
        variant: "danger",
      });
      setMessage(["", ""]);
      setIsSendingMessage(false);
      return;
    }

    const newChat = {
      chatId: response.data.chatId,
      history: response.data.history,
      chatName: response.data.chatName,
    };
    if (!chatId) {
      // Creating a new chat
      // setAllChats((chats) => {
      //   console.log({ chats });
      //   return [...chats, newChat];
      // });
      console.log("---- Creating a new chat ----");
      setChat(newChat);
      router.push(`/chat/${response.data.chatId}`);
    }
    setChat(newChat);
    setMessage(["", ""]);
    setIsSendingMessage(false);
  };

  const deleteChat = async (chatId: UUID) => {
    try {
      await axiosInstance.delete(`/chat/${chatId}`);
      setAllChats((chats) => chats.filter((chat) => chat.chatId !== chatId));
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
    console.log(chatId);
    if (chatId) {
      fetchChat(chatId);
    }
  }, [fetchAllChats, fetchChat, chatId]);

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
