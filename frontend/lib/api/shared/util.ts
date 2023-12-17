import { ChatItem, ChatMessageItem } from "@/app/chat/[chatId]/types";
export const getFirstChatMessageItem = (
  ChatItems: ChatItem[]
): ChatMessageItem[] => {
  if (ChatItems.length === 0) {
    return [];
  }
  const messageItems = ChatItems.filter(
    (item: ChatItem) => item.item_type === "MESSAGE"
  ) as ChatMessageItem[];

  return messageItems;
};
