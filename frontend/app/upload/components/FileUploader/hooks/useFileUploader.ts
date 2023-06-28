/* eslint-disable */
import { redirect } from "next/navigation";
import { useCallback, useState } from "react";
import { FileRejection, useDropzone } from "react-dropzone";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useAxios, useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";
import { useFeature } from "@growthbook/growthbook-react";
import { UUID } from "crypto";

export const useFileUploader = () => {
  const { track } = useEventTracking();
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const [files, setFiles] = useState<File[]>([]);
  const { session } = useSupabase();

  const { currentBrain, createBrain } = useBrainContext();
  const { axiosInstance } = useAxios();

  const shouldUseMultipleBrains = useFeature("multiple-brains").on;

  if (session === null) {
    redirect("/login");
  }

  const upload = useCallback(
    async (file: File, brainId: UUID) => {
      const formData = new FormData();
      formData.append("uploadFile", file);
      try {
        void track("FILE_UPLOADED");
        const response = await axiosInstance.post(
          `/upload/?brain_id=${brainId}`,
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
      } catch (error: unknown) {
        publish({
          variant: "danger",
          text: "Failed to upload file: " + JSON.stringify(error),
        });
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
      setFiles([]);
      await Promise.all(files.map((file) => upload(file, currentBrain?.id)));
    }
    console.log("Please select or create a brain to upload a file");

    if (currentBrain?.id === undefined && shouldUseMultipleBrains !== true) {
      const createdBrainId = await createBrain("Default");
      createdBrainId
        ? await Promise.all(files.map((file) => upload(file, createdBrainId)))
        : null;
      setFiles([]);
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
