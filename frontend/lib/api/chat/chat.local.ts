import { ChatConfig } from "@/lib/context/ChatProvider/types";
const chatConfigLocalStorageKey = "chat-config";

type PartialChatConfig = Partial<ChatConfig>;

export const saveChatsConfigInLocalStorage = (
  chatConfig: PartialChatConfig
): void => {
  localStorage.setItem(chatConfigLocalStorageKey, JSON.stringify(chatConfig));
};

export const getChatsConfigFromLocalStorage = ():
  | PartialChatConfig
  | undefined => {
  try {
    const config = localStorage.getItem(chatConfigLocalStorageKey);

    if (config === null) {
      return undefined;
    }

    return JSON.parse(config) as PartialChatConfig;
  } catch (error) {
    return undefined;
  }
};
