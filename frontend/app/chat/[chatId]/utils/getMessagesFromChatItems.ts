import { ChatItem, ChatMessage } from "../types";

export const getMessagesFromChatItems = (
  chatItems: ChatItem[]
): ChatMessage[] => {
  const messages = chatItems
    .filter((item) => item.item_type === "MESSAGE")
    .map((item) => item.body as ChatMessage);

  return messages;
};
