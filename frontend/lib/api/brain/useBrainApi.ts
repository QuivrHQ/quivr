import { useAxios } from "@/lib/hooks";

import {
  addBrainSubscriptions,
  createBrain,
  deleteBrain,
  getBrain,
  getBrainDocuments,
  getBrains,
  getBrainUsers,
  getDefaultBrain,
  Subscription,
} from "./brain";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainApi = () => {
  const { axiosInstance } = useAxios();

  return {
    getBrainDocuments: async (brainId: string) =>
      getBrainDocuments(brainId, axiosInstance),
    createBrain: async (name: string) => createBrain(name, axiosInstance),
    deleteBrain: async (id: string) => deleteBrain(id, axiosInstance),
    getDefaultBrain: async () => getDefaultBrain(axiosInstance),
    getBrains: async () => getBrains(axiosInstance),
    getBrain: async (id: string) => getBrain(id, axiosInstance),
    addBrainSubscriptions: async (
      brainId: string,
      subscriptions: Subscription[]
    ) => addBrainSubscriptions(brainId, subscriptions, axiosInstance),
    getBrainUsers: async (brainId: string) =>
      getBrainUsers(brainId, axiosInstance),
  };
};
