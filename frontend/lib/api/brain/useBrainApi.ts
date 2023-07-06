import { useAxios } from "@/lib/hooks";

import { getBrainDocuments } from "./brain";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainApi = () => {
  const { axiosInstance } = useAxios();

  return {
    getBrainDocuments: async (brainId: string) =>
      getBrainDocuments(brainId, axiosInstance),
  };
};
