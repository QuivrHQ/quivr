import { useSupabase } from "@/app/supabase-provider";
import { useToast } from "@/lib/hooks/useToast";
import { useAxios } from "@/lib/useAxios";
import { redirect } from "next/navigation";
import { useCallback, useState } from "react";
import { FileRejection, useDropzone } from "react-dropzone";

export const useFileUploader = () => {
  const [isPending, setIsPending] = useState(false);
  const { publish } = useToast();
  const [files, setFiles] = useState<File[]>([]);
  const [pendingFileIndex, setPendingFileIndex] = useState<number>(0);
  const { session } = useSupabase();

  const { axiosInstance } = useAxios();

  if (session === null) {
    redirect("/login");
  }

  const upload = useCallback(
    async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      try {
        const response = await axiosInstance.post(`/upload`, formData);

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

    for (const file of files) {
      await upload(file);
      setPendingFileIndex((i) => i + 1);
    }
    setPendingFileIndex(0);
    setFiles([]);
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
    pendingFileIndex,

    files,
    setFiles,
  };
};
