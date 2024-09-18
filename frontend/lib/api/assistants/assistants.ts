import { AxiosInstance } from "axios";

import { Assistant } from "@/app/quality-assistant/types/assistant";

export const getAssistants = async (
  axiosInstance: AxiosInstance
): Promise<Assistant[]> => {
  return (await axiosInstance.get<Assistant[]>(`/assistants`)).data;
};
