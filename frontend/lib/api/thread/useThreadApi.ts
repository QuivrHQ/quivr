import { useAxios } from "@/lib/hooks";

import {
  addQuestionAndAnswer,
  QuestionAndAnwser,
} from "./addQuestionAndAnswer";
import {
  addQuestion,
  AddQuestionParams,
  createThread,
  deleteThread,
  getThreadItems,
  getThreads,
  ThreadUpdatableProperties,
  updateThread,
} from "./thread";

// TODO: split './thread.ts' into multiple files, per function for example
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThreadApi = () => {
  const { axiosInstance } = useAxios();

  return {
    createThread: async (threadName: string) =>
      createThread(threadName, axiosInstance),
    getThreads: async () => getThreads(axiosInstance),
    deleteThread: async (threadId: string) =>
      deleteThread(threadId, axiosInstance),
    addQuestion: async (props: AddQuestionParams) =>
      addQuestion(props, axiosInstance),
    getThreadItems: async (threadId: string) =>
      getThreadItems(threadId, axiosInstance),
    updateThread: async (threadId: string, props: ThreadUpdatableProperties) =>
      updateThread(threadId, props, axiosInstance),
    addQuestionAndAnswer: async (
      threadId: string,
      questionAndAnswer: QuestionAndAnwser
    ) => addQuestionAndAnswer(threadId, questionAndAnswer, axiosInstance),
  };
};
