import { AxiosInstance } from "axios";

import {
  ThreadEntity,
  ThreadItem,
  ThreadMessage,
  ThreadQuestion,
} from "@/app/thread/[threadId]/types";

export const createThread = async (
  name: string,
  axiosInstance: AxiosInstance
): Promise<ThreadEntity> => {
  const createdThread = (
    await axiosInstance.post<ThreadEntity>("/thread", { name: name })
  ).data;

  return createdThread;
};

export const getThreads = async (
  axiosInstance: AxiosInstance
): Promise<ThreadEntity[]> => {
  const response = await axiosInstance.get<{
    threads: ThreadEntity[];
  }>(`/thread`);

  return response.data.threads;
};

export const deleteThread = async (
  threadId: string,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.delete(`/thread/${threadId}`);
};

export type AddQuestionParams = {
  threadId: string;
  threadQuestion: ThreadQuestion;
  brainId: string;
};

export const addQuestion = async (
  { threadId, threadQuestion, brainId }: AddQuestionParams,
  axiosInstance: AxiosInstance
): Promise<ThreadMessage> => {
  const response = await axiosInstance.post<ThreadMessage>(
    `/thread/${threadId}/question?brain_id=${brainId}`,
    threadQuestion
  );

  return response.data;
};

export const getThreadItems = async (
  threadId: string,
  axiosInstance: AxiosInstance
): Promise<ThreadItem[]> =>
  (await axiosInstance.get<ThreadItem[]>(`/thread/${threadId}/history`)).data;

export type ThreadUpdatableProperties = {
  thread_name?: string;
};
export const updateThread = async (
  threadId: string,
  thread: ThreadUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<ThreadEntity> => {
  return (
    await axiosInstance.put<ThreadEntity>(
      `/thread/${threadId}/metadata`,
      thread
    )
  ).data;
};
