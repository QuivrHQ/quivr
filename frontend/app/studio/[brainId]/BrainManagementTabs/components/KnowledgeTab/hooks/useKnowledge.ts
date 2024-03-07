import { useQuery, useQueryClient } from "@tanstack/react-query";
import { UUID } from "crypto";

import { getKnowledgeDataKey } from "@/lib/api/knowledge/config";
import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledge = ({ brainId }: { brainId?: UUID }) => {
  const queryClient = useQueryClient();

  const { getAllKnowledge } = useKnowledgeApi();
  const { data: allKnowledge, isLoading: isPending } = useQuery({
    queryKey: [getKnowledgeDataKey(brainId!)],
    queryFn: () => getAllKnowledge({ brainId: brainId! }),
    enabled: brainId !== undefined,
  });

  if (brainId === undefined) {
    return {
      invalidateKnowledgeDataKey: () => void {},
      isPending: false,
      allKnowledge: [],
    };
  }

  const knowledge_data_key = getKnowledgeDataKey(brainId);

  const invalidateKnowledgeDataKey = () => {
    void queryClient.invalidateQueries({ queryKey: [knowledge_data_key] });
  };

  return {
    invalidateKnowledgeDataKey,
    isPending,
    allKnowledge: allKnowledge ?? [],
  };
};
