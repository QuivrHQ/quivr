import { useToast } from "@/app/hooks/useToast";
import { useSupabase } from "@/app/supabase-provider";
import axios from "axios";
import { redirect } from "next/navigation";
import { useCallback, useState } from "react";
import { FileRejection, useDropzone } from "react-dropzone";

export const useFileUploader = () => {
  const [isPending, setIsPending] = useState(false);
  const { messageToast, setMessage } = useToast();
  const [files, setFiles] = useState<File[]>([]);
  const [pendingFileIndex, setPendingFileIndex] = useState<number>(0);
  const { session } = useSupabase();

  if (session === null) {
    redirect("/login");
  }

  const upload = useCallback(
    async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      try {
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/upload`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${session.access_token}`,
            },
          }
        );

        setMessage({
          type: response.data.type,
          text:
            (response.data.type === "success"
              ? "File uploaded successfully: "
              : "") + JSON.stringify(response.data.message),
        });
      } catch (error: unknown) {
        setMessage({
          type: "error",
          text: "Failed to upload file: " + JSON.stringify(error),
        });
      }
    },
    [session.access_token]
  );

  const onDrop = (acceptedFiles: File[], fileRejections: FileRejection[]) => {
    if (fileRejections.length > 0) {
      setMessage({ type: "error", text: "File too big." });
      return;
    }
    setMessage(null);
    for (let i = 0; i < acceptedFiles.length; i++) {
      const file = acceptedFiles[i];
      const isAlreadyInFiles =
        files.filter((f) => f.name === file.name && f.size === file.size)
          .length > 0;
      if (isAlreadyInFiles) {
        setMessage({
          type: "warning",
          text: `${file.name} was already added`,
        });
        acceptedFiles.splice(i, 1);
      }
    }
    setFiles((files) => [...files, ...acceptedFiles]);
  };

  const uploadAllFiles = async () => {
    setIsPending(true);
    setMessage(null);
    // files.forEach((file) => upload(file));
    for (const file of files) {
      await upload(file);
      setPendingFileIndex((i) => i + 1);
    }
    setPendingFileIndex(0);
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
    messageToast,
    files,
    setFiles,
  };
};
