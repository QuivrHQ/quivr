import { AxiosInstance } from "axios";

import {
  ChatEntity,
  ChatHistory,
  ChatQuestion,
} from "@/app/chat/[chatId]/types";

export const createChat = async (
  name: string,
  axiosInstance: AxiosInstance
): Promise<ChatEntity> => {
  const createdChat = (
    await axiosInstance.post<ChatEntity>("/chat", { name: name })
  ).data;

  return createdChat;
};

export const getChats = async (
  axiosInstance: AxiosInstance
): Promise<ChatEntity[]> => {
  const response = await axiosInstance.get<{
    chats: ChatEntity[];
  }>(`/chat`);

  return response.data.chats;
};

export const deleteChat = async (
  chatId: string,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.delete(`/chat/${chatId}`);
};

export type AddQuestionParams = {
  chatId: string;
  chatQuestion: ChatQuestion;
  brainId: string;
};

export const addQuestion = async (
  { chatId, chatQuestion, brainId }: AddQuestionParams,
  axiosInstance: AxiosInstance
): Promise<ChatHistory> => {
  const response = await axiosInstance.post<ChatHistory>(
    `/chat/${chatId}/question?brain_id=${brainId}`,
    chatQuestion
  );

  return response.data;
};

export const getHistory = async (
  chatId: string,
  axiosInstance: AxiosInstance
): Promise<ChatHistory[]> =>
  (await axiosInstance.get<ChatHistory[]>(`/chat/${chatId}/history`)).data;

export type ChatUpdatableProperties = {
  chat_name?: string;
};
export const updateChat = async (
  chatId: string,
  chat: ChatUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<ChatEntity> => {
  return (await axiosInstance.put<ChatEntity>(`/chat/${chatId}/metadata`, chat))
    .data;
};
