import { ChatHistory, ChatItem } from "../types";

export const getMessagesFromChatHistory = (
  chatHistory: ChatItem[]
): ChatHistory[] => {
  const messages = chatHistory
    .filter((item) => item.item_type === "MESSAGE")
    .map((item) => item.body as ChatHistory);

  return messages;
};
