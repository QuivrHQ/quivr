import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

export type UploadResponse = {
  data: { type: ToastData["variant"]; message: ToastData["text"] };
};

export type UploadInputProps = {
  brainId: UUID;
  formData: FormData;
};

export const uploadFile = async (
  props: UploadInputProps,
  axiosInstance: AxiosInstance
): Promise<UploadResponse> =>
  axiosInstance.post(`/upload?brain_id=${props.brainId}`, props.formData);
