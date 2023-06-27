import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useAxios } from "@/lib/hooks";

import { ChatEntity, ChatHistory, ChatQuestion } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatService = () => {
  const { axiosInstance } = useAxios();
  const { currentBrain } = useBrainContext();
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
    if (currentBrain?.id === undefined) {
      throw new Error("No current brain");
    }

    return (
      await axiosInstance.post<ChatHistory>(
        `/chat/${chatId}/question/?brain_id=${currentBrain.id}`,
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
