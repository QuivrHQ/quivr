import { getChatsConfigFromLocalStorage } from "@/lib/api/chat/chat.local";
import { useUserData } from "@/lib/hooks/useUserData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLocalStorageChatConfig = () => {
  const { userData } = useUserData();

  const chatConfig = getChatsConfigFromLocalStorage();

  const model = (userData?.models ?? []).includes(chatConfig?.model ?? "")
    ? chatConfig?.model
    : undefined;

  return {
    chatConfig: {
      model: model,
      temperature: chatConfig?.temperature,
      maxTokens: chatConfig?.maxTokens,
    },
  };
};
