"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { getMessagesFromChatItems } from "@/app/chat/[chatId]/utils/getMessagesFromChatItems";
import { getNotificationsFromChatItems } from "@/app/chat/[chatId]/utils/getNotificationsFromChatItems";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatContext } from "@/lib/context";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSharedChatItems = () => {
  const { setMessages, setNotifications } = useChatContext();
  const { getSharedChatItems } = useChatApi();
  const [isLoading, setIsLoading] = useState(false);
  const { publish } = useToast();

  const params = useParams();

  const sharedCode = params?.sharedCode as string | undefined;

  useEffect(() => {
    const fetchHistory = async () => {
      if (sharedCode === undefined) {
        setMessages([]);
        setNotifications([]);

        return;
      }

      try {
        setIsLoading(true);
        const chatItems = await getSharedChatItems(sharedCode);

        setMessages(getMessagesFromChatItems(chatItems));
        setNotifications(getNotificationsFromChatItems(chatItems));
      } catch (e) {
        publish({
          variant: "danger",
          text: JSON.stringify(e),
        });
      } finally {
        setIsLoading(false);
      }
    };
    void fetchHistory();
  }, [sharedCode]);

  return {
    isLoading,
  };
};
