import { useAxios } from "@/lib/hooks";

import { getThreadNotifications } from "./notification";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useNotificationApi = () => {
  const { axiosInstance } = useAxios();

  return {
    getThreadNotifications: async (threadId: string) =>
      await getThreadNotifications(threadId, axiosInstance),
  };
};
