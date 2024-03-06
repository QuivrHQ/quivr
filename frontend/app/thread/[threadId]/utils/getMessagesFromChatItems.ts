import { ThreadItem, ThreadMessage } from "../types";

export const getMessagesFromThreadItems = (
  threadItems: ThreadItem[]
): ThreadMessage[] => {
  const messages = threadItems
    .filter((item) => item.item_type === "MESSAGE")
    .map((item) => item.body as ThreadMessage);

  return messages;
};
