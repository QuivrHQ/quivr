import { useParams } from "next/navigation";
import { useEffect } from "react";

import { getMessagesFromChatItems } from "@/app/chat/[chatId]/utils/getMessagesFromChatItems";
import { getNotificationsFromChatItems } from "@/app/chat/[chatId]/utils/getNotificationsFromChatItems";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatContext } from "@/lib/context";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSharedChatItems = () => {
  const { setMessages, setNotifications } = useChatContext();
  const { getSharedChatItems } = useChatApi();

  const params = useParams();

  const sharedCode = params?.sharedCode as string | undefined;

  useEffect(() => {
    const fetchHistory = async () => {
      if (sharedCode === undefined) {
        setMessages([]);
        setNotifications([]);

        return;
      }

      const chatItems = await getSharedChatItems(sharedCode);

      setMessages(getMessagesFromChatItems(chatItems));
      setNotifications(getNotificationsFromChatItems(chatItems));
    };
    void fetchHistory();
  }, [sharedCode]);
};
