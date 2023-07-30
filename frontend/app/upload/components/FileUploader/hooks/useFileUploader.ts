/* eslint-disable */
import { useCallback, useState } from "react";
import { FileRejection, useDropzone } from "react-dropzone";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useAxios, useToast } from "@/lib/hooks";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { useEventTracking } from "@/services/analytics/useEventTracking";
import axios from "axios";
import { UUID } from "crypto";

export const useFileUploader = () => {
  const { track } = useEventTracking();
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const [files, setFiles] = useState<File[]>([]);
  const { session } = useSupabase();

  const { currentBrain } = useBrainContext();
  const { axiosInstance } = useAxios();

  if (session === null) {
    redirectToLogin();
  }

  const upload = useCallback(
    async (file: File, brainId: UUID) => {
      const formData = new FormData();
      formData.append("uploadFile", file);
      try {
        void track("FILE_UPLOADED");
        const response = await axiosInstance.post(
          `/upload?brain_id=${brainId}`,
          formData
        );
        track("FILE_UPLOADED");
        publish({
          variant: response.data.type,
          text:
            (response.data.type === "success"
              ? "File uploaded successfully: "
              : "") + JSON.stringify(response.data.message),
        });
      } catch (e: unknown) {
        if (axios.isAxiosError(e) && e.response?.status === 403) {
          publish({
            variant: "danger",
            text: `${JSON.stringify(
              (
                e.response as {
                  data: { detail: string };
                }
              ).data.detail
            )}`,
          });
        } else {
          publish({
            variant: "danger",
            text: "Failed to upload file: " + JSON.stringify(e),
          });
        }
      }
    },
    [session.access_token, publish]
  );

  const onDrop = (acceptedFiles: File[], fileRejections: FileRejection[]) => {
    if (fileRejections.length > 0) {
      publish({ variant: "danger", text: "File too big." });

      return;
    }

    for (let i = 0; i < acceptedFiles.length; i++) {
      const file = acceptedFiles[i];
      const isAlreadyInFiles =
        files.filter((f) => f.name === file.name && f.size === file.size)
          .length > 0;
      if (isAlreadyInFiles) {
        publish({
          variant: "warning",
          text: `${file.name} was already added`,
        });
        acceptedFiles.splice(i, 1);
      }
    }
    setFiles((files) => [...files, ...acceptedFiles]);
  };

  const uploadAllFiles = async () => {
    if (files.length === 0) {
      publish({
        text: "Please, add files to upload",
        variant: "warning",
      });

      return;
    }
    setIsPending(true);
    if (currentBrain?.id !== undefined) {
      await Promise.all(files.map((file) => upload(file, currentBrain?.id)));
      setFiles([]);
    } else {
      publish({
        text: "Please, select or create a brain to upload a file",
        variant: "warning",
      });
    }
    setIsPending(false);
  };

  const { getInputProps, getRootProps, isDragActive, open } = useDropzone({
    onDrop,
    noClick: true,
    maxSize: 100000000, // 1 MB
  });

  return {
    isPending,
    getInputProps,
    getRootProps,
    isDragActive,
    open,
    uploadAllFiles,

    files,
    setFiles,
  };
};
