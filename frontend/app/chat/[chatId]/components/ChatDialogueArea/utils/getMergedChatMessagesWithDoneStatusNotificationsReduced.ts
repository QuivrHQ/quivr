import {
  ChatItem,
  ChatMessage,
  ChatMessageItem,
  Notification,
  NotificationItem,
} from "../../../types";
import { ChatItemWithGroupedNotifications } from "../types";

// Function to create a ChatMessageItem from a message
const createChatMessageItem = (message: ChatMessage): ChatMessageItem => ({
  item_type: "MESSAGE",
  body: message,
});

// Function to create a NotificationItem from a notification
const createNotificationItem = (
  notification: Notification
): NotificationItem => ({
  item_type: "NOTIFICATION",
  body: notification,
});

// Function to merge chat messages and notifications into a single array
const mergeChatMessagesAndNotifications = (
  messages: ChatMessage[],
  notifications: Notification[]
): ChatItem[] => [
  ...messages.map(createChatMessageItem),
  ...notifications.map(createNotificationItem),
];

// Function to compare two items by timestamp (message_time or datetime)
const compareItemsByTimestamp = (a: ChatItem, b: ChatItem): number => {
  const timestampA =
    a.item_type === "MESSAGE" ? a.body.message_time : a.body.datetime;
  const timestampB =
    b.item_type === "MESSAGE" ? b.body.message_time : b.body.datetime;

  return Date.parse(timestampA) - Date.parse(timestampB);
};

// Main function to get merged chat messages with reduced notifications using reduce
export const getMergedChatMessagesWithDoneStatusNotificationsReduced = (
  messages: ChatMessage[],
  notifications: Notification[]
): ChatItemWithGroupedNotifications[] => {
  const mergedChatItems = mergeChatMessagesAndNotifications(
    messages,
    notifications.filter((notification) => notification.status === "Done")
  );
  mergedChatItems.sort(compareItemsByTimestamp);

  // Group notifications between messages
  const groupedChatItemsByNotifications = mergedChatItems.reduce(
    (result, item) => {
      if (item.item_type === "MESSAGE") {
        result.push(item);
      } else {
        const lastItem = result[result.length - 1];
        if (lastItem !== undefined && lastItem.item_type === "NOTIFICATION") {
          lastItem.body.push(item.body);
        } else {
          result.push({
            item_type: "NOTIFICATION",
            body: [item.body],
          });
        }
      }

      return result;
    },
    [] as ChatItemWithGroupedNotifications[]
  );

  return groupedChatItemsByNotifications;
};
