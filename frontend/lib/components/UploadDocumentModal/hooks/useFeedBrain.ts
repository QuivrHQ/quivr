import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useThreadApi } from "@/lib/api/thread/useThreadApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useToast } from "@/lib/hooks";
import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";

import { useFeedBrainHandler } from "./useFeedBrainHandler";

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
  let { brainId } = useUrlBrain();
  const { currentBrainId } = useBrainContext();
  const { setKnowledgeToFeed, knowledgeToFeed, setShouldDisplayFeedCard } =
    useKnowledgeToFeedContext();
  const [hasPendingRequests, setHasPendingRequests] = useState(false);
  const { handleFeedBrain } = useFeedBrainHandler();

  const { createThread, deleteThread } = useThreadApi();

  const feedBrain = async (): Promise<void> => {
    brainId ??= currentBrainId ?? undefined;
    if (brainId === undefined) {
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

    //TODO: Modify backend archi to avoid creating a thread for each feed action
    const currentThreadId = (await createThread("New Thread")).thread_id;

    try {
      dispatchHasPendingRequests?.();
      closeFeedInput?.();
      setHasPendingRequests(true);
      setShouldDisplayFeedCard(false);
      await handleFeedBrain({
        brainId,
        threadId: currentThreadId,
      });

      setKnowledgeToFeed([]);
    } catch (e) {
      publish({
        variant: "danger",
        text: JSON.stringify(e),
      });
    } finally {
      setHasPendingRequests(false);
      await deleteThread(currentThreadId);
    }
  };

  return {
    feedBrain,
    hasPendingRequests,
    setHasPendingRequests,
  };
};
