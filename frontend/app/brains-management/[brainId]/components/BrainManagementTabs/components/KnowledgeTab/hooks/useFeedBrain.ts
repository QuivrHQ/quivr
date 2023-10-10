import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useKnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput/hooks/useKnowledgeToFeedInput.ts";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useToast } from "@/lib/hooks";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { useKnowledgeToFeed } from "./useKnowledgeToFeed";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedBrain = ({
  dispatchHasPendingRequests,
  closeFeedInput,
}: {
  dispatchHasPendingRequests?: () => void;
  closeFeedInput?: () => void;
}) => {
  const { publish } = useToast();
  const { files, urls } = useKnowledgeToFeed();
  const { t } = useTranslation(["upload"]);
  const { updateOnboarding, onboarding } = useOnboarding();
  const { currentBrainId } = useBrainContext();
  const { setKnowledgeToFeed, knowledgeToFeed } = useKnowledgeToFeedContext();
  const [hasPendingRequests, setHasPendingRequests] = useState(false);

  const { createChat, deleteChat } = useChatApi();

  const { crawlWebsiteHandler, uploadFileHandler } = useKnowledgeToFeedInput();

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
