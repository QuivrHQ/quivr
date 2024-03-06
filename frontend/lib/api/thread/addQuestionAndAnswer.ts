import { AxiosInstance } from "axios";

import { ThreadMessage } from "@/app/thread/[threadId]/types";

export type QuestionAndAnwser = {
  question: string;
  answer: string;
};

export const addQuestionAndAnswer = async (
  threadId: string,
  questionAndAnswer: QuestionAndAnwser,
  axiosInstance: AxiosInstance
): Promise<ThreadMessage> => {
  const response = await axiosInstance.post<ThreadMessage>(
    `/thread/${threadId}/question/answer`,
    questionAndAnswer
  );

  return response.data;
};
