import { useEffect } from "react";

import { useKnowledge } from "@/app/studio/[brainId]/BrainManagementTabs/components/KnowledgeTab/hooks/useKnowledge";
import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";

import { useFeedBrain } from "./useFeedBrain";

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
