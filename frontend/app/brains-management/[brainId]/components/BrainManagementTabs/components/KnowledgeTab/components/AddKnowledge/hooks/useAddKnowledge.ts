import { useEffect } from "react";

import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";

import { useFeedBrain } from "./useFeedBrain";
import { useKnowledge } from "../../../hooks/useKnowledge";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddKnowledge = () => {
  const { brainId } = useUrlBrain();
  const { invalidateKnowledgeDataKey } = useKnowledge({
    brainId,
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
