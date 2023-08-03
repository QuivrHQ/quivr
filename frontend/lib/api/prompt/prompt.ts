import { AxiosInstance } from "axios";

import { Prompt } from "@/lib/types/Prompt";

export type CreatePromptProps = {
  title: string;
  content: string;
};

export const createPrompt = async (
  prompt: CreatePromptProps,
  axiosInstance: AxiosInstance
): Promise<Prompt> => {
  return (await axiosInstance.post<Prompt>("/prompts", prompt)).data;
};

export const getPrompt = async (
  promptId: string,
  axiosInstance: AxiosInstance
): Promise<Prompt | undefined> => {
  return (await axiosInstance.get<Prompt>(`/prompts/${promptId}`)).data;
};

export type PromptUpdatableProperties = {
  title: string;
  content: string;
};
export const updatePrompt = async (
  promptId: string,
  prompt: PromptUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<Prompt> => {
  return (await axiosInstance.put<Prompt>(`/prompts/${promptId}`, prompt)).data;
};

export const getPublicPrompts = async (
  axiosInstance: AxiosInstance
): Promise<Prompt[]> => {
  return (await axiosInstance.get<Prompt[]>("/prompts")).data;
};
