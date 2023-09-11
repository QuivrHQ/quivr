import { ChatItem, Notification } from "../types";

export const getNotificationsFromChatHistory = (
  chatHistory: ChatItem[]
): Notification[] => {
  const messages = chatHistory
    .filter((item) => item.item_type === "NOTIFICATION")
    .map((item) => item.body as Notification);

  return messages;
};
