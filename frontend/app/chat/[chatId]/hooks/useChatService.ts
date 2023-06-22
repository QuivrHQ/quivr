import { useAxios } from "@/lib/hooks";

import { ChatEntity, ChatHistory, ChatQuestion } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatService = () => {
  const { axiosInstance } = useAxios();

  const createChat = async ({ name }: { name: string }) => {
    return axiosInstance.post<ChatEntity>(`/chat`, { name });
  };

  const getChatHistory = async (chatId: string | undefined) => {
    if (chatId === undefined) {
      return [];
    }
    const rep = (
      await axiosInstance.get<ChatHistory[]>(`/chat/${chatId}/history`)
    ).data;

    return rep;
  };
  const addQuestion = async (
    chatId: string,
    chatQuestion: ChatQuestion
  ): Promise<ChatHistory> => {
    return (
      await axiosInstance.post<ChatHistory>(
        `/chat/${chatId}/question`,
        chatQuestion
      )
    ).data;
  };

  return {
    createChat,
    getChatHistory,
    addQuestion,
  };
};
