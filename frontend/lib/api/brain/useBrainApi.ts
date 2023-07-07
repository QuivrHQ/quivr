import { UUID } from "crypto";

import { useAxios } from "@/lib/hooks";

import {
  createBrain,
  deleteBrain,
  getBrain,
  getBrainDocuments,
  getBrains,
  getDefaultBrain,
} from "./brain";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainApi = () => {
  const { axiosInstance } = useAxios();

  return {
    getBrainDocuments: async (brainId: string) =>
      getBrainDocuments(brainId, axiosInstance),
    createBrain: async (name: string) => createBrain(name, axiosInstance),
    deleteBrain: async (id: UUID) => deleteBrain(id, axiosInstance),
    getDefaultBrain: async () => getDefaultBrain(axiosInstance),
    getBrains: async () => getBrains(axiosInstance),
    getBrain: async (id: UUID) => getBrain(id, axiosInstance),
  };
};
