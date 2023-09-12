import { useParams } from "next/navigation";
import { useEffect } from "react";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatContext } from "@/lib/context";

import { getMessagesFromChatItems } from "../utils/getMessagesFromChatItems";
import { getNotificationsFromChatItems } from "../utils/getNotificationsFromChatItems";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSelectedChatPage = () => {
  const { setMessages, setNotifications } = useChatContext();
  const { getChatItems } = useChatApi();

  const params = useParams();
  const chatId = params?.chatId as string | undefined;

  useEffect(() => {
    const fetchHistory = async () => {
      if (chatId === undefined) {
        setMessages([]);
        setNotifications([]);

        return;
      }

      const chatItems = await getChatItems(chatId);

      setMessages(getMessagesFromChatItems(chatItems));
      setNotifications(getNotificationsFromChatItems(chatItems));
    };
    void fetchHistory();
  }, [chatId, setMessages]);
};
