import { ChatConfig } from "@/lib/context/ChatProvider/types";
const chatConfigLocalStorageKey = "chat-config";
export const saveChatsConfigInLocalStorage = (chatConfig: ChatConfig): void => {
  localStorage.setItem(chatConfigLocalStorageKey, JSON.stringify(chatConfig));
};

export const getChatsConfigFromLocalStorage = (): ChatConfig | undefined => {
  const config = localStorage.getItem(chatConfigLocalStorageKey);

  if (config === null) {
    return undefined;
  }

  return JSON.parse(config) as ChatConfig;
};
