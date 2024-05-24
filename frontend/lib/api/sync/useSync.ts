import { useAxios } from "@/lib/hooks";

import { getUserSyncs, syncGoogleDrive, syncSharepoint } from "./sync";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSync = () => {
  const { axiosInstance } = useAxios();

  const iconUrls = {
    googleDrive:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/gdrive_8316d080fd.png",
    azure:
      "https://quivr-cms.s3.eu-west-3.amazonaws.com/sharepoint_8c41cfdb09.png",
  };

  return {
    syncGoogleDrive: async (name: string) =>
      syncGoogleDrive(name, axiosInstance),
    syncSharepoint: async (name: string) => syncSharepoint(name, axiosInstance),
    getUserSyncs: async () => getUserSyncs(axiosInstance),
    iconUrls,
  };
};
