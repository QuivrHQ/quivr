import { AxiosInstance } from "axios";

import { BrainsUsages } from "./types";

export const getBrainsUsages = async (
  axiosInstance: AxiosInstance,
  brain_id?: string
): Promise<BrainsUsages | undefined> => {
  const brainsUsages = (
    await axiosInstance.get<BrainsUsages | undefined>(
      `/analytics/brains-usages/${brain_id}`
    )
  ).data;

  return brainsUsages;
};
