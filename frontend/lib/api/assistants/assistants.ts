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

  // Créer un tableau pour stocker les fichiers (conserver leurs types natifs File/Blob)
  const filesArray: File[] = [];
  processAssistantInput.files.forEach((file) => {
    filesArray.push(file);
  });

  // Ajout du tableau de fichiers sous une seule clé `files[]`
  formData.append("files[]", JSON.stringify(filesArray));

  // Ajouter les autres données
  formData.append("input", JSON.stringify(processAssistantInput.input));

  return (
    await axiosInstance.post<string>(`/assistants/task`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
  ).data;
};
