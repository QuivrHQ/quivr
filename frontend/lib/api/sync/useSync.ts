import { UUID } from "crypto";

import { useAxios } from "@/lib/hooks";

import {
  deleteActiveSync,
  deleteUserSync,
  getActiveSyncs,
  getSyncFiles,
  getUserSyncs,
  syncFiles,
  syncGoogleDrive,
  syncSharepoint,
  updateActiveSync,
} from "./sync";
import { OpenedConnection, Provider } from "./types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSync = () => {
  const { axiosInstance } = useAxios();

  const iconUrls: Record<Provider, string> = {
    Google:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/gdrive_8316d080fd.png",
    Azure:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/sharepoint_8c41cfdb09.png",
  };

  const getActiveSyncsForBrain = async (brainId: string) => {
    const activeSyncs = await getActiveSyncs(axiosInstance);

    return activeSyncs.filter((sync) => sync.brain_id === brainId);
  };

  return {
    syncGoogleDrive: async (name: string) =>
      syncGoogleDrive(name, axiosInstance),
    syncSharepoint: async (name: string) => syncSharepoint(name, axiosInstance),
    getUserSyncs: async () => getUserSyncs(axiosInstance),
    getSyncFiles: async (userSyncId: number, folderId?: string) =>
      getSyncFiles(axiosInstance, userSyncId, folderId),
    iconUrls,
    syncFiles: async (openedConnection: OpenedConnection, brainId: UUID) =>
      syncFiles(axiosInstance, openedConnection, brainId),
    getActiveSyncs: async () => getActiveSyncs(axiosInstance),
    getActiveSyncsForBrain,
    deleteUserSync: async (syncId: number) =>
      deleteUserSync(axiosInstance, syncId),
    deleteActiveSync: async (syncId: number) =>
      deleteActiveSync(axiosInstance, syncId),
    updateActiveSync: async (openedConnection: OpenedConnection) =>
      updateActiveSync(axiosInstance, openedConnection),
  };
};
