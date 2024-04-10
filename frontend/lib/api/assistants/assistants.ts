import { AxiosInstance } from "axios";

import { Assistant } from "./types";

export const getAssistants = async (
  axiosInstance: AxiosInstance
): Promise<Assistant | undefined> => {
  return (await axiosInstance.get<Assistant | undefined>("/assistants/")).data;
};
