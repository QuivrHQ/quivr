import { AxiosInstance } from "axios";

import {
  Assistant,
  ProcessAssistantInput,
} from "@/app/quality-assistant/types/assistant";
import { Process } from "@/app/quality-assistant/types/process";

export const getAssistants = async (
  axiosInstance: AxiosInstance
): Promise<Assistant[]> => {
  return (await axiosInstance.get<Assistant[]>(`/assistants`)).data;
};

export const getTasks = async (
  axiosInstance: AxiosInstance
): Promise<Process[]> => {
  return (await axiosInstance.get<Process[]>(`/assistants/tasks`)).data;
};

export const processTask = async (
  axiosInstance: AxiosInstance,
  processAssistantInput: ProcessAssistantInput
): Promise<string> => {
  const formData = new FormData();

  formData.append("input", JSON.stringify(processAssistantInput.input));

  processAssistantInput.files.forEach((file) => {
    if (file instanceof File) {
      formData.append("files", file);
    } else {
      console.error("L'élément n'est pas un fichier valide", file);
    }
  });

  const response = await axiosInstance.post<string>(
    `/assistants/task`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const deleteTask = async (
  axiosInstance: AxiosInstance,
  taskId: number
): Promise<void> => {
  await axiosInstance.delete(`/assistants/task/${taskId}`);
};

export const downloadTaskResult = async (
  axiosInstance: AxiosInstance,
  taskId: number
): Promise<string> => {
  return (await axiosInstance<string>(`/assistants/task/${taskId}/download`))
    .data;
};
