/*eslint max-lines: ["error", 200 ]*/

import { useQueryClient } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useNotificationApi } from "@/lib/api/notification/useNotificationApi";
import { CHATS_DATA_KEY } from "@/lib/api/thread/config";
import { useThreadApi } from "@/lib/api/thread/useThreadApi";
import { useKnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput/hooks/useKnowledgeToFeedInput.ts";
import { useThreadContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useToast } from "@/lib/hooks";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { FeedItemCrawlType, FeedItemUploadType } from "../../../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedBrainInThread = ({
  dispatchHasPendingRequests,
}: {
  dispatchHasPendingRequests: () => void;
}) => {
  const { publish } = useToast();
  const queryClient = useQueryClient();
  const { t } = useTranslation(["upload"]);
  const router = useRouter();
  const { updateOnboarding, onboarding } = useOnboarding();
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { currentBrainId } = useBrainContext();
  const { setKnowledgeToFeed, knowledgeToFeed } = useKnowledgeToFeedContext();
  const [hasPendingRequests, setHasPendingRequests] = useState(false);
  const { createThread } = useThreadApi();
  const params = useParams();
  const threadId = params?.threadId as UUID | undefined;
  const { setNotifications } = useThreadContext();
  const { getThreadNotifications } = useNotificationApi();
  const fetchNotifications = async (currentThreadId: UUID): Promise<void> => {
    const fetchedNotifications = await getThreadNotifications(currentThreadId);
    setNotifications(fetchedNotifications);
  };
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
    try {
      dispatchHasPendingRequests();
      setShouldDisplayFeedCard(false);
      setHasPendingRequests(true);
      const currentThreadId =
        threadId ?? (await createThread("New Thread")).thread_id;
      const uploadPromises = files.map((file) =>
        uploadFileHandler(file, currentBrainId, currentThreadId)
      );
      const crawlPromises = urls.map((url) =>
        crawlWebsiteHandler(url, currentBrainId, currentThreadId)
      );

      const updateOnboardingPromise = async () => {
        if (onboarding.onboarding_a) {
          await updateOnboarding({
            onboarding_a: false,
          });
        }
      };

      await Promise.all([
        ...uploadPromises,
        ...crawlPromises,
        updateOnboardingPromise(),
      ]);

      setKnowledgeToFeed([]);

      if (threadId === undefined) {
        void queryClient.invalidateQueries({
          queryKey: [CHATS_DATA_KEY],
        });
        void router.push(`/thread/${currentThreadId}`);
      } else {
        await fetchNotifications(currentThreadId);
      }
    } catch (e) {
      publish({
        variant: "danger",
        text: JSON.stringify(e),
      });
    } finally {
      setHasPendingRequests(false);
    }
  };

  return {
    feedBrain,
    hasPendingRequests,
  };
};
