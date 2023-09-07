import { ChatItem } from "../../../types";

export const checkIfHasPendingRequest = (chatItems: ChatItem[]): boolean => {
  return chatItems.some(
    (item) =>
      item.item_type === "NOTIFICATION" && item.body.status === "Pending"
  );
};
