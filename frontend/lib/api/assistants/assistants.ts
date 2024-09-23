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
