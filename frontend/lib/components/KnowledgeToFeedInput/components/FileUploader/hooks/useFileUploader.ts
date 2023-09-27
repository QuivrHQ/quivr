/* eslint-disable max-lines */

import { FileRejection, useDropzone } from "react-dropzone";
import { useTranslation } from "react-i18next";

import { useKnowledgeContext } from "@/lib/context/KnowledgeProvider/hooks/useKnowledgeContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

import { FeedItemUploadType } from "../../../../../../app/chat/[chatId]/components/ActionsBar/types";
import { acceptedFormats } from "../helpers/acceptedFormats";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFileUploader = () => {
  const { knowledgeToFeed, addKnowledgeToFeed } = useKnowledgeContext();

  const files: File[] = (
    knowledgeToFeed.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

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
        addKnowledgeToFeed({
          source: "upload",
          file: file,
        });
      }
    }
  };

  const { getInputProps, getRootProps, isDragActive, open } = useDropzone({
    onDrop,
    noClick: true,
    maxSize: 100000000, // 1 MB
    accept: acceptedFormats,
  });

  return {
    getInputProps,
    getRootProps,
    isDragActive,
    open,
  };
};
