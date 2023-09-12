import { ChatItem, ChatMessage } from "../types";

export const getMessagesFromChatHistory = (
  chatHistory: ChatItem[]
): ChatMessage[] => {
  const messages = chatHistory
    .filter((item) => item.item_type === "MESSAGE")
    .map((item) => item.body as ChatMessage);

  return messages;
};
