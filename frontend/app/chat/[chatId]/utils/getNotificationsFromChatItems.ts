import { ChatItem, Notification } from "../types";

export const getNotificationsFromChatItems = (
  chatItems: ChatItem[]
): Notification[] => {
  const messages = chatItems
    .filter((item) => item.item_type === "NOTIFICATION")
    .map((item) => item.body as Notification);

  return messages;
};
