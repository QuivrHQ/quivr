import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

export type UploadResponse = {
  data: { type: ToastData["variant"]; message: ToastData["text"] };
};

export type UploadInputProps = {
  brainId: UUID;
  formData: FormData;
  chat_id?: UUID;
};

export const uploadFile = async (
  props: UploadInputProps,
  axiosInstance: AxiosInstance
): Promise<UploadResponse> => {
  let uploadUrl = `/upload?brain_id=${props.brainId}`;
  if (props.chat_id !== undefined) {
    uploadUrl = uploadUrl.concat(`&chat_id=${props.chat_id}`);
  }

  return axiosInstance.post(uploadUrl, props.formData);
};
