import { useAxios } from "@/lib/hooks";

import { getAssistants } from "./assistants";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAssistants = () => {
  const { axiosInstance } = useAxios();

  return {
    getBrainsUsages: async () => getAssistants(axiosInstance),
  };
};
