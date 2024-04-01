import { useAxios } from "@/lib/hooks";

import { getBrainsUsages } from "./analytics";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAnalytics = () => {
  const { axiosInstance } = useAxios();

  return {
    getBrainsUsages: async () => getBrainsUsages(axiosInstance),
  };
};
