import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { useChatApi } from "@/lib/api/chat/useChatApi";
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
  const { openedConnections } = useFromConnectionsContext();

  const { createChat, deleteChat } = useChatApi();

  const feedBrain = async (): Promise<void> => {
    brainId ??= currentBrainId ?? undefined;
    if (brainId === undefined) {
      publish({
        variant: "danger",
        text: t("selectBrainFirst"),
      });

      return;
    }

    if (knowledgeToFeed.length === 0 && !openedConnections.length) {
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
      await handleFeedBrain({
        brainId,
        chatId: currentChatId,
      });
      setShouldDisplayFeedCard(false);
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
