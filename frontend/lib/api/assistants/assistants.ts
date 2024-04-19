import { AxiosInstance } from "axios";

import { Assistant, ProcessAssistantRequest } from "./types";

export const getAssistants = async (
  axiosInstance: AxiosInstance
): Promise<Assistant[] | undefined> => {
  return (await axiosInstance.get<Assistant[] | undefined>("/assistants")).data;
};

export const processAssistant = async (
  axiosInstance: AxiosInstance,
  input: ProcessAssistantRequest,
  files: File[]
): Promise<string | undefined> => {
  const formData = new FormData();

  formData.append(
    "input",
    JSON.stringify({
      name: input.name,
      inputs: {
        files: input.inputs.files,
        urls: input.inputs.urls,
        texts: input.inputs.texts,
      },
      outputs: input.outputs,
    })
  );

  files.forEach((file) => {
    formData.append("files", file);
  });

  return (
    await axiosInstance.post<string | undefined>("/assistant/process", formData)
  ).data;
};
