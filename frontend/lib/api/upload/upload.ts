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
): Promise<UploadResponse> =>
  axiosInstance.post(
    `/upload?brain_id=${props.brainId}&chat_id=${props.chat_id ?? ""}`,
    props.formData
  );
