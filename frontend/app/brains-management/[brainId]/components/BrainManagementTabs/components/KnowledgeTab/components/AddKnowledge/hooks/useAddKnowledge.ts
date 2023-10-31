import { useEffect } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useFeedBrain } from "./useFeedBrain";
import { useKnowledge } from "../../../hooks/useKnowledge";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddKnowledge = () => {
  const { currentBrain } = useBrainContext();
  const { invalidateKnowledgeDataKey } = useKnowledge({
    brainId: currentBrain?.id,
  });

  const { feedBrain, hasPendingRequests, setHasPendingRequests } = useFeedBrain(
    {
      dispatchHasPendingRequests: () => setHasPendingRequests(true),
    }
  );

  useEffect(() => {
    if (!hasPendingRequests) {
      invalidateKnowledgeDataKey();
    }
  }, [hasPendingRequests, invalidateKnowledgeDataKey]);

  return {
    feedBrain,
    hasPendingRequests,
  };
};
