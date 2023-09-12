import {
  ChatItem,
  ChatMessage,
  ChatMessageItem,
  Notification,
  NotificationItem,
} from "../../../types";

type ChatItemWithGroupedNotifications =
  | ChatMessageItem
  | {
      item_type: "NOTIFICATION";
      body: Notification[];
    };

export const getMergedChatHistoryWithReducedNotifications = (
  messages: ChatMessage[],
  notifications: Notification[]
): ChatItemWithGroupedNotifications[] => {
  const mergedChatItems: ChatItem[] = [
    ...messages.map(
      (message) => ({ item_type: "MESSAGE", body: message } as ChatMessageItem)
    ),
    ...notifications.map(
      (notification) =>
        ({ item_type: "NOTIFICATION", body: notification } as NotificationItem)
    ),
  ];

  // Sort all items by message_time (or datetime) in ascending order
  mergedChatItems.sort((a, b) => {
    const timestampA =
      a.item_type === "MESSAGE" ? a.body.message_time : a.body.datetime;
    const timestampB =
      b.item_type === "MESSAGE" ? b.body.message_time : b.body.datetime;

    return Date.parse(timestampA) - Date.parse(timestampB);
  });

  const groupedChatHistory: ChatItemWithGroupedNotifications[] = [];

  for (const item of mergedChatItems) {
    if (item.item_type === "MESSAGE") {
      groupedChatHistory.push(item);
    } else {
      const lastItemIndex = groupedChatHistory.length - 1;
      const lastItem =
        lastItemIndex >= 0 ? groupedChatHistory[lastItemIndex] : null;

      if (
        lastItem !== null &&
        lastItem !== undefined &&
        lastItem.item_type === "NOTIFICATION"
      ) {
        lastItem.body.push(item.body);
      } else {
        groupedChatHistory.push({
          item_type: "NOTIFICATION",
          body: [item.body],
        });
      }
    }
  }

  return groupedChatHistory;
};
