import { useAxios } from "@/lib/hooks";

import {
  createPrompt,
  CreatePromptProps,
  getPrompt,
  getPublicPrompts,
  PromptUpdatableProperties,
  updatePrompt,
} from "./prompt";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePromptApi = () => {
  const { axiosInstance } = useAxios();

  return {
    createPrompt: async (prompt: CreatePromptProps) =>
      createPrompt(prompt, axiosInstance),
    getPrompt: async (promptId: string) => getPrompt(promptId, axiosInstance),
    updatePrompt: async (promptId: string, prompt: PromptUpdatableProperties) =>
      updatePrompt(promptId, prompt, axiosInstance),
    getPublicPrompts: async () => await getPublicPrompts(axiosInstance),
  };
};
