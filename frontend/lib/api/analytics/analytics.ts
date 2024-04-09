import { AxiosInstance } from "axios";

import { BrainsUsages, Range } from "./types";

export const getBrainsUsages = async (
  axiosInstance: AxiosInstance,
  brain_id: string | null,
  graph_range: Range
): Promise<BrainsUsages | undefined> => {
  const brainsUsages = (
    await axiosInstance.get<BrainsUsages | undefined>(
      `/analytics/brains-usages?brain_id=${brain_id}&graph_range=${graph_range}`
    )
  ).data;

  return brainsUsages;
};
