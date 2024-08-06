import { AxiosInstance } from "axios";

import { Model } from "@/lib/types/Models";

export const getModels = async (
  axiosInstance: AxiosInstance
): Promise<Model[]> => {
  return (await axiosInstance.get<Model[]>(`/notifications`)).data;
};
