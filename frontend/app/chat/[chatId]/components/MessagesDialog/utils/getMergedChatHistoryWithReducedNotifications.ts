/* eslint-disable complexity */
import { ChatHistory, ChatItem, Notification } from "../../../types";

export const getMergedChatHistoryWithReducedNotifications = (
  messages: ChatHistory[],
  notifications: Notification[]
): ChatItem[] => {
  const mergedChatItems: ChatItem[] = [];
  let currentNotification: Notification | null = null;

  const allItems: (ChatHistory | Notification)[] = [
    ...messages,
    ...notifications,
  ];

  // Sort all items by message_time (or datetime) in ascending order
  allItems.sort((a, b) => {
    const timestampA = "message_time" in a ? a.message_time : a.datetime;
    const timestampB = "message_time" in b ? b.message_time : b.datetime;

    return Date.parse(timestampA) - Date.parse(timestampB);
  });

  for (const item of allItems) {
    if ("user_message" in item && "assistant" in item) {
      // It's a chat message
      if (currentNotification) {
        addNotification(mergedChatItems, currentNotification);
        currentNotification = null;
      }
      addChatMessage(mergedChatItems, item);
    } else if ("action" in item && "status" in item) {
      // It's a notification
      if (currentNotification) {
        mergeNotification(currentNotification, item);
      } else {
        currentNotification = item;
      }
    }
  }

  // Add the last notification if it exists
  if (currentNotification) {
    addNotification(mergedChatItems, currentNotification);
  }

  return mergedChatItems;
};

const addChatMessage = (mergedChatItems: ChatItem[], message: ChatHistory) => {
  mergedChatItems.push({
    item_type: "MESSAGE",
    body: message,
  });
};

const addNotification = (
  mergedChatItems: ChatItem[],
  notification: Notification
) => {
  mergedChatItems.push({
    item_type: "NOTIFICATION",
    body: notification,
  });
};

const mergeNotification = (
  existingNotification: Notification,
  newNotification: Notification
) => {
  if ("message" in existingNotification) {
    existingNotification.message += `\n${newNotification.message ?? ""}`;
  }
};
