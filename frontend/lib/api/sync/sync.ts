import { AxiosInstance } from "axios";

import { Sync, SyncElements } from "./types";

export const syncGoogleDrive = async (
  name: string,
  axiosInstance: AxiosInstance
): Promise<{ authorization_url: string }> => {
  return (
    await axiosInstance.post<{ authorization_url: string }>(
      `/sync/google/authorize?name=${name}`
    )
  ).data;
};

export const syncSharepoint = async (
  name: string,
  axiosInstance: AxiosInstance
): Promise<{ authorization_url: string }> => {
  return (
    await axiosInstance.post<{ authorization_url: string }>(
      `/sync/azure/authorize?name=${name}`
    )
  ).data;
};

export const getUserSyncs = async (
  axiosInstance: AxiosInstance
): Promise<Sync[]> => {
  return (await axiosInstance.get<Sync[]>("/sync")).data;
};

export const getSyncFiles = async (
  axiosInstance: AxiosInstance,
  userSyncId: number
): Promise<SyncElements> => {
  return (
    await axiosInstance.get<SyncElements>(
      `/sync/${userSyncId}/files?user_sync_id=${userSyncId}`
    )
  ).data;
};
