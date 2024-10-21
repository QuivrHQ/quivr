import { UUID } from "crypto";

import { useAxios } from "@/lib/hooks";

import {
  deleteActiveSync,
  deleteUserSync,
  getActiveSyncs,
  getSyncFiles,
  getUserSyncs,
  syncDropbox,
  syncFiles,
  syncGoogleDrive,
  syncNotion,
  syncSharepoint,
  updateActiveSync,
} from "./sync";
import { OpenedConnection } from "./types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSync = () => {
  const { axiosInstance } = useAxios();

  const providerIconUrls: Record<string, string> = {
    google:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/gdrive_8316d080fd.png",
    azure:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/sharepoint_8c41cfdb09.png",
    dropbox:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/dropbox_dce4f3d753.png",
    notion:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/Notion_app_logo_004168672c.png",
    github:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/dropbox_dce4f3d753.png",
  };

  const getActiveSyncsForBrain = async (brainId: string) => {
    const activeSyncs = await getActiveSyncs(axiosInstance);

    return activeSyncs.filter((sync) => sync.brain_id === brainId);
  };

  return {
    syncGoogleDrive: async (name: string) =>
      syncGoogleDrive(name, axiosInstance),
    syncSharepoint: async (name: string) => syncSharepoint(name, axiosInstance),
    syncDropbox: async (name: string) => syncDropbox(name, axiosInstance),
    syncNotion: async (name: string) => syncNotion(name, axiosInstance),
    getUserSyncs: async () => getUserSyncs(axiosInstance),
    getSyncFiles: async (userSyncId: number, folderId?: string) =>
      getSyncFiles(axiosInstance, userSyncId, folderId),
    providerIconUrls,
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
