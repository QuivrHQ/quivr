import { useAxios } from "@/lib/hooks";

import { getAssistants, processAssistant } from "./assistants";
import { ProcessAssistantRequest } from "./types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAssistants = () => {
  const { axiosInstance } = useAxios();

  return {
    getAssistants: async () => getAssistants(axiosInstance),
    processAssistant: async (input: ProcessAssistantRequest, files: File[]) =>
      processAssistant(axiosInstance, input, files),
  };
};
