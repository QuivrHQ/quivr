import { useAxios } from "@/lib/hooks";

import { createApiKey } from "./auth";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAuthApi = () => {
  const { axiosInstance } = useAxios();

  return {
    createApiKey: async () => createApiKey(axiosInstance),
  };
};
