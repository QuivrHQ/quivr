import { Notification, ThreadItem } from "../types";

export const getNotificationsFromThreadItems = (
  threadItems: ThreadItem[]
): Notification[] => {
  const messages = threadItems
    .filter((item) => item.item_type === "NOTIFICATION")
    .map((item) => item.body as Notification);

  return messages;
};
