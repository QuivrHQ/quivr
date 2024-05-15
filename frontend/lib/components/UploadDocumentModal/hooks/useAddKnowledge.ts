import { UUID } from "crypto";
import { useEffect } from "react";

import { useAddedKnowledge } from "@/lib/hooks/useAddedKnowledge";
import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";

import { useFeedBrain } from "./useFeedBrain";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddKnowledge = (inputBrainId?: UUID) => {
  const { brainId: urlBrainId } = useUrlBrain();
  const brainId = inputBrainId ?? urlBrainId;

  const { invalidateKnowledgeDataKey } = useAddedKnowledge({
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
