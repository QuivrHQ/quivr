import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useEffect } from "react";

import { useNotificationApi } from "@/lib/api/notification/useNotificationApi";
import { useThreadApi } from "@/lib/api/thread/useThreadApi";
import { useThreadContext } from "@/lib/context";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import { getThreadNotificationsQueryKey } from "../utils/getChatNotificationsQueryKey";
import { getMessagesFromThreadItems } from "../utils/getMessagesFromChatItems";
import { getNotificationsFromThreadItems } from "../utils/getNotificationsFromChatItems";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThreadNotificationsSync = () => {
  const { setMessages, setNotifications, notifications } = useThreadContext();
  const { getThreadItems } = useThreadApi();
  const { getThreadNotifications } = useNotificationApi();
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const params = useParams();
  const threadId = params?.threadId as string | undefined;

  const threadNotificationsQueryKey = getThreadNotificationsQueryKey(
    threadId ?? ""
  );
  const { data: fetchedNotifications = [] } = useQuery({
    queryKey: [threadNotificationsQueryKey],
    enabled: notifications.length > 0,
    queryFn: () => {
      if (threadId === undefined) {
        return [];
      }

      return getThreadNotifications(threadId);
    },
    refetchInterval: () => {
      if (notifications.length === 0) {
        return false;
      }
      const hasAPendingNotification = notifications.find(
        (item) => item.status === "Pending"
      );

      if (hasAPendingNotification) {
        return 2_000; // in ms
      }

      return false;
    },
  });

  useEffect(() => {
    if (fetchedNotifications.length === 0) {
      return;
    }
    setNotifications(fetchedNotifications);
  }, [fetchedNotifications]);

  useEffect(() => {
    setShouldDisplayFeedCard(false);
    const fetchHistory = async () => {
      if (threadId === undefined) {
        setMessages([]);
        setNotifications([]);

        return;
      }
      const threadItems = await getThreadItems(threadId);
      const messagesFromThreadItems = getMessagesFromThreadItems(threadItems);
      if (
        messagesFromThreadItems.length > 1 ||
        (messagesFromThreadItems[0] &&
          messagesFromThreadItems[0].assistant !== "")
      ) {
        setMessages(messagesFromThreadItems);
        setNotifications(getNotificationsFromThreadItems(threadItems));
      }
    };
    void fetchHistory();
  }, [threadId]);
};
