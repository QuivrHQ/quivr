import { AxiosInstance } from "axios";

import { Notification } from "@/app/thread/[threadId]/types";

export const getThreadNotifications = async (
  threadId: string,
  axiosInstance: AxiosInstance
): Promise<Notification[]> => {
  return (await axiosInstance.get<Notification[]>(`/notifications/${threadId}`))
    .data;
};
