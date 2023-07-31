import { ChatConfig } from "@/lib/context/ChatProvider/types";

export const saveChatConfigInLocalStorage = (
  chatId: string,
  chatConfig: ChatConfig
): void => {
  localStorage.setItem(`chat-config-${chatId}`, JSON.stringify(chatConfig));
};

export const getChatConfigFromLocalStorage = (
  chatId: string
): ChatConfig | undefined => {
  const config = localStorage.getItem(`chat-config-${chatId}`);

  if (config === null) {
    return undefined;
  }

  return JSON.parse(config) as ChatConfig;
};
