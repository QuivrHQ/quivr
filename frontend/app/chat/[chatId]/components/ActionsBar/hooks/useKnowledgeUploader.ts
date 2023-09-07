/* eslint-disable max-lines */
import axios from "axios";
import { UUID } from "crypto";
import { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { useCrawlApi } from "@/lib/api/crawl/useCrawlApi";
import { useUploadApi } from "@/lib/api/upload/useUploadApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useToast } from "@/lib/hooks";

import { FeedItemCrawlType, FeedItemType, FeedItemUploadType } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeUploader = () => {
  const [contents, setContents] = useState<FeedItemType[]>([]);
  const { publish } = useToast();
  const { uploadFile } = useUploadApi();
  const { t } = useTranslation(["upload"]);
  const { crawlWebsiteUrl } = useCrawlApi();

  const { currentBrainId } = useBrainContext();
  const addContent = (content: FeedItemType) => {
    setContents((prevContents) => [...prevContents, content]);
  };
  const removeContent = (index: number) => {
    setContents((prevContents) => prevContents.filter((_, i) => i !== index));
  };

  const crawlWebsiteHandler = useCallback(
    async (url: string, brainId: UUID) => {
      // Configure parameters
      const config = {
        url: url,
        js: false,
        depth: 1,
        max_pages: 100,
        max_time: 60,
      };

      try {
        await crawlWebsiteUrl({
          brainId,
          config,
        });
      } catch (error: unknown) {
        publish({
          variant: "danger",
          text: t("crawlFailed", {
            message: JSON.stringify(error),
            ns: "upload",
          }),
        });
      }
    },
    [crawlWebsiteUrl, publish, t]
  );

  const uploadFileHandler = useCallback(
    async (file: File, brainId: UUID) => {
      const formData = new FormData();
      formData.append("uploadFile", file);
      try {
        await uploadFile({
          brainId: brainId,
          formData,
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
            text: t("error", { message: e, ns: "upload" }),
          });
        }
      }
    },
    [publish, t, uploadFile]
  );

  const files: File[] = (
    contents.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

  const urls: string[] = (
    contents.filter((c) => c.source === "crawl") as FeedItemCrawlType[]
  ).map((c) => c.url);

  const feedBrain = async (): Promise<void> => {
    if (currentBrainId === null) {
      publish({
        variant: "danger",
        text: t("selectBrainFirst"),
      });

      return;
    }
    try {
      await Promise.all([
        ...files.map((file) => uploadFileHandler(file, currentBrainId)),
        ...urls.map((url) => crawlWebsiteHandler(url, currentBrainId)),
      ]);
    } catch (e: unknown) {
      publish({
        variant: "danger",
        text: JSON.stringify(e),
      });
    }
  };

  return {
    addContent,
    contents,
    removeContent,
    feedBrain,
  };
};
