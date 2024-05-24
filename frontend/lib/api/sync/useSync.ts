import { useAxios } from "@/lib/hooks";

import {
  getSyncFiles,
  getUserSyncs,
  syncGoogleDrive,
  syncSharepoint,
} from "./sync";
import { Provider } from "./types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSync = () => {
  const { axiosInstance } = useAxios();

  const iconUrls: Record<Provider, string> = {
    Google:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/gdrive_8316d080fd.png",
    Azure:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/sharepoint_8c41cfdb09.png",
  };

  return {
    syncGoogleDrive: async (name: string) =>
      syncGoogleDrive(name, axiosInstance),
    syncSharepoint: async (name: string) => syncSharepoint(name, axiosInstance),
    getUserSyncs: async () => getUserSyncs(axiosInstance),
    getSyncFiles: async (userSyncId: number) =>
      getSyncFiles(axiosInstance, userSyncId),
    iconUrls,
  };
};
