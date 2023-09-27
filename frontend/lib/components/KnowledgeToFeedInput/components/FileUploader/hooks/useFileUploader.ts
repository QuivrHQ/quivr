/* eslint-disable max-lines */

import { FileRejection, useDropzone } from "react-dropzone";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { SupportedFileExtensionsWithDot } from "@/lib/types/SupportedFileExtensions";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

import { FeedItemType } from "../../../../../../app/chat/[chatId]/components/ActionsBar/types";

type UseFileUploaderProps = {
  addContent: (content: FeedItemType) => void;
  files: File[];
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFileUploader = ({
  addContent,
  files,
}: UseFileUploaderProps) => {
  const { publish } = useToast();
  const { session } = useSupabase();
  const { track } = useEventTracking();

  if (session === null) {
    redirectToLogin();
  }

  const { t } = useTranslation(["upload"]);

  const onDrop = (acceptedFiles: File[], fileRejections: FileRejection[]) => {
    if (fileRejections.length > 0) {
      const firstRejection = fileRejections[0];

      if (firstRejection.errors[0].code === "file-invalid-type") {
        publish({ variant: "danger", text: t("invalidFileType") });
      } else {
        publish({
          variant: "danger",
          text: t("maxSizeError", { ns: "upload" }),
        });
      }

      return;
    }

    for (const file of acceptedFiles) {
      const isAlreadyInFiles =
        files.filter((f) => f.name === file.name && f.size === file.size)
          .length > 0;
      if (isAlreadyInFiles) {
        publish({
          variant: "warning",
          text: t("alreadyAdded", { fileName: file.name, ns: "upload" }),
        });
      } else {
        void track("FILE_UPLOADED");
        addContent({
          source: "upload",
          file: file,
        });
      }
    }
  };

  const accept: Record<string, SupportedFileExtensionsWithDot[]> = {
    "text/plain": [".txt"],
    "text/csv": [".csv"],
    "text/markdown": [".md", ".markdown"],
    "audio/x-m4a": [".m4a"],
    "audio/mpeg": [".mp3", ".mpga", ".mpeg"],
    "audio/webm": [".webm"],
    "video/mp4": [".mp4"],
    "audio/wav": [".wav"],
    "application/pdf": [".pdf"],
    "text/html": [".html"],
    "application/vnd.openxmlformats-officedocument.presentationml.presentation":
      [".pptx"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
      ".docx",
    ],
    "application/vnd.oasis.opendocument.text": [".odt"],
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
      ".xlsx",
      ".xls",
    ],
    "application/epub+zip": [".epub"],
    "application/x-ipynb+json": [".ipynb"],
    "text/x-python": [".py"],
  };

  const { getInputProps, getRootProps, isDragActive, open } = useDropzone({
    onDrop,
    noClick: true,
    maxSize: 100000000, // 1 MB
    accept,
  });

  return {
    getInputProps,
    getRootProps,
    isDragActive,
    open,
  };
};
