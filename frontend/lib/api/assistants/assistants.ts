import { AxiosInstance } from "axios";

import {
  Assistant,
  ProcessAssistantInput,
} from "@/app/quality-assistant/types/assistant";

export const getAssistants = async (
  axiosInstance: AxiosInstance
): Promise<Assistant[]> => {
  return (await axiosInstance.get<Assistant[]>(`/assistants`)).data;
};

export const getTasks = async (
  axiosInstance: AxiosInstance
): Promise<string> => {
  return (await axiosInstance.get<string>(`/assistants/tasks`)).data;
};

export const processTask = async (
  axiosInstance: AxiosInstance,
  processAssistantInput: ProcessAssistantInput
): Promise<string> => {
  return (
    await axiosInstance.post<string>(`/assistants/task`, processAssistantInput)
  ).data;
};
