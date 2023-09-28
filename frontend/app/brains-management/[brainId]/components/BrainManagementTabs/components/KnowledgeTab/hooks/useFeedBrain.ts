import { useState } from "react";
import { useTranslation } from "react-i18next";

import {
  FeedItemCrawlType,
  FeedItemUploadType,
} from "@/app/chat/[chatId]/components/ActionsBar/types";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useKnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput/hooks/useKnowledgeToFeedInput.ts";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedBrain = ({
  dispatchHasPendingRequests,
  closeFeedInput,
}: {
  dispatchHasPendingRequests?: () => void;
  closeFeedInput?: () => void;
}) => {
  const { publish } = useToast();
  const { t } = useTranslation(["upload"]);

  const { currentBrainId } = useBrainContext();
  const { setKnowledgeToFeed, knowledgeToFeed } = useKnowledgeToFeedContext();
  const [hasPendingRequests, setHasPendingRequests] = useState(false);

  const { createChat, deleteChat } = useChatApi();

  const { crawlWebsiteHandler, uploadFileHandler } = useKnowledgeToFeedInput();

  const files: File[] = (
    knowledgeToFeed.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

  const urls: string[] = (
    knowledgeToFeed.filter((c) => c.source === "crawl") as FeedItemCrawlType[]
  ).map((c) => c.url);

  const feedBrain = async (): Promise<void> => {
    if (currentBrainId === null) {
      publish({
        variant: "danger",
        text: t("selectBrainFirst"),
      });

      return;
    }

    if (knowledgeToFeed.length === 0) {
      publish({
        variant: "danger",
        text: t("addFiles"),
      });

      return;
    }

    //TODO: Modify backend archi to avoid creating a chat for each feed action
    const currentChatId = (await createChat("New Chat")).chat_id;

    try {
      dispatchHasPendingRequests?.();
      closeFeedInput?.();
      setHasPendingRequests(true);
      const uploadPromises = files.map((file) =>
        uploadFileHandler(file, currentBrainId, currentChatId)
      );
      const crawlPromises = urls.map((url) =>
        crawlWebsiteHandler(url, currentBrainId, currentChatId)
      );

      await Promise.all([...uploadPromises, ...crawlPromises]);

      setKnowledgeToFeed([]);
    } catch (e) {
      publish({
        variant: "danger",
        text: JSON.stringify(e),
      });
    } finally {
      setHasPendingRequests(false);
      await deleteChat(currentChatId);
    }
  };

  return {
    feedBrain,
    hasPendingRequests,
    setHasPendingRequests,
  };
};
