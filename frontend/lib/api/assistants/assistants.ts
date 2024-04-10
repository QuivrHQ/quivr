import { AxiosInstance } from "axios";

import { Assistants } from "./types";

export const getAssistants = async (
  axiosInstance: AxiosInstance
): Promise<Assistants | undefined> => {
  return (await axiosInstance.get<Assistants | undefined>("/assistants/")).data;
};
