import { ProcessAssistantInput } from "@/app/quality-assistant/types/assistant";
import { useAxios } from "@/lib/hooks";

import {
  deleteTask,
  downloadTaskResult,
  getAssistants,
  getTasks,
  processTask,
} from "./assistants";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAssistants = () => {
  const { axiosInstance } = useAxios();

  return {
    getAssistants: async () => getAssistants(axiosInstance),
    getTasks: async () => getTasks(axiosInstance),
    processTask: async (processAssistantInput: ProcessAssistantInput) =>
      processTask(axiosInstance, processAssistantInput),
    deleteTask: async (taskId: number) => deleteTask(axiosInstance, taskId),
    downloadTaskResult: async (taskId: number) =>
      downloadTaskResult(axiosInstance, taskId),
  };
};
