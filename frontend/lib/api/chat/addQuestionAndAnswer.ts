import { AxiosInstance } from "axios";

import { ChatMessage } from "@/app/chat/[chatId]/types";

export type QuestionAndAnwser = {
  question: string;
  answer: string;
};

export const addQuestionAndAnswer = async (
  chatId: string,
  questionAndAnswer: QuestionAndAnwser,
  axiosInstance: AxiosInstance
): Promise<ChatMessage> => {
  const response = await axiosInstance.post<ChatMessage>(
    `/chat/${chatId}/question/answer`,
    questionAndAnswer
  );

  return response.data;
};
