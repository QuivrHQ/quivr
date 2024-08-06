import { useAxios } from "@/lib/hooks";

import { getModels } from "./models";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAssistants = () => {
  const { axiosInstance } = useAxios();

  return {
    getAssistants: async () => getModels(axiosInstance),
  };
};
