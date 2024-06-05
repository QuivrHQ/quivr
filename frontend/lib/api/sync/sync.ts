import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { OpenedConnection } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/FromConnection-provider";

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
  userSyncId: number,
  folderId?: string
): Promise<SyncElements> => {
  const url = folderId
    ? `/sync/${userSyncId}/files?user_sync_id=${userSyncId}&folder_id=${folderId}`
    : `/sync/${userSyncId}/files?user_sync_id=${userSyncId}`;

  return (await axiosInstance.get<SyncElements>(url)).data;
};

export const syncFiles = async (
  axiosInstance: AxiosInstance,
  openedConnection: OpenedConnection,
  brainId: UUID
): Promise<void> => {
  return (
    await axiosInstance.post<void>(`/sync/active`, {
      name: openedConnection.name,
      syncs_user_id: openedConnection.id,
      settings: {},
      brain_id: brainId,
    })
  ).data;
};
