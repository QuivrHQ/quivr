import { AxiosInstance } from "axios";

import { BrainsUsages } from "./types";

export const getBrainsUsages = async (
  axiosInstance: AxiosInstance
): Promise<BrainsUsages | undefined> => {
  const brainsUsages = (
    await axiosInstance.get<BrainsUsages | undefined>(
      `/analytics/brains-usages`
    )
  ).data;

  return brainsUsages;
};
