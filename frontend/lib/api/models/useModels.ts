import { useAxios } from "@/lib/hooks";

import { getModels } from "./models";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useModels = () => {
  const { axiosInstance } = useAxios();

  return {
    getModels: async () => getModels(axiosInstance),
  };
};
