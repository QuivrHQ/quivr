import { useEffect, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useFeedBrain } from "../../../hooks/useFeedBrain";
import { useKnowledge } from "../../../hooks/useKnowledge";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddKnowledge = () => {
  const [shouldDisplayModal, setShouldDisplayModal] = useState(false);
  const { currentBrain } = useBrainContext();
  const { invalidateKnowledgeDataKey } = useKnowledge({
    brainId: currentBrain?.id,
  });

  const { feedBrain, hasPendingRequests, setHasPendingRequests } = useFeedBrain(
    {
      dispatchHasPendingRequests: () => setHasPendingRequests(true),
      closeFeedInput: () => setShouldDisplayModal(false),
    }
  );

  useEffect(() => {
    if (!hasPendingRequests) {
      invalidateKnowledgeDataKey();
    }
  }, [hasPendingRequests, invalidateKnowledgeDataKey]);

  return {
    shouldDisplayModal,
    setShouldDisplayModal,
    feedBrain,
    hasPendingRequests,
  };
};
