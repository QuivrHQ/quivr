import { useParams } from "next/navigation";
import { useEffect } from "react";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatContext } from "@/lib/context";

import { getMessagesFromChatHistory } from "../utils/getMessagesFromChatHistory";
import { getNotificationsFromChatHistory } from "../utils/getNotificationsFromChatHistory";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSelectedChatPage = () => {
  const { setMessages, setNotifications } = useChatContext();
  const { getHistory } = useChatApi();

  const params = useParams();
  const chatId = params?.chatId as string | undefined;

  useEffect(() => {
    const fetchHistory = async () => {
      if (chatId === undefined) {
        setMessages([]);

        return;
      }

      const chatHistory = await getHistory(chatId);

      if (chatHistory.length > 0) {
        setMessages(getMessagesFromChatHistory(chatHistory));
        setNotifications(getNotificationsFromChatHistory(chatHistory));
      }
    };
    void fetchHistory();
  }, [chatId, setMessages]);
};
