import { useAxios } from "@/lib/hooks";

import { uploadFile, UploadInputProps } from "./upload";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUploadApi = () => {
  const { axiosInstance } = useAxios();

  return {
    uploadFile: async (props: UploadInputProps) =>
      uploadFile(props, axiosInstance),
  };
};
