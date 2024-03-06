import {
  Notification,
  NotificationItem,
  ThreadItem,
  ThreadMessage,
  ThreadMessageItem,
} from "../../../types";
import { ThreadItemWithGroupedNotifications } from "../types";

// Function to create a ThreadMessageItem from a message
const createThreadMessageItem = (
  message: ThreadMessage
): ThreadMessageItem => ({
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

// Function to merge thread messages and notifications into a single array
const mergeThreadMessagesAndNotifications = (
  messages: ThreadMessage[],
  notifications: Notification[]
): ThreadItem[] => [
  ...messages.map(createThreadMessageItem),
  ...notifications.map(createNotificationItem),
];

// Function to compare two items by timestamp (message_time or datetime)
const compareItemsByTimestamp = (a: ThreadItem, b: ThreadItem): number => {
  const timestampA =
    a.item_type === "MESSAGE" ? a.body.message_time : a.body.datetime;
  const timestampB =
    b.item_type === "MESSAGE" ? b.body.message_time : b.body.datetime;

  return Date.parse(timestampA) - Date.parse(timestampB);
};

// Main function to get merged thread messages with reduced notifications using reduce
export const getMergedThreadMessagesWithDoneStatusNotificationsReduced = (
  messages: ThreadMessage[],
  notifications: Notification[]
): ThreadItemWithGroupedNotifications[] => {
  const mergedThreadItems = mergeThreadMessagesAndNotifications(
    messages,
    notifications.filter((notification) => notification.status === "Done")
  );
  mergedThreadItems.sort(compareItemsByTimestamp);

  // Group notifications between messages
  const groupedThreadItemsByNotifications = mergedThreadItems.reduce(
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
    [] as ThreadItemWithGroupedNotifications[]
  );

  return groupedThreadItemsByNotifications;
};
