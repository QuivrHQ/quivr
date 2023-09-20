import { useQuery } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useEffect, useState } from "react";

import { getKnowledgeDataKey } from "@/lib/api/knowledge/config";
import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { Knowledge } from "@/lib/types/Knowledge";

type useKnowledgeTabProps = {
  brainId: UUID;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeTab = ({ brainId }: useKnowledgeTabProps) => {
  const [allKnowledge, setAllKnowledge] = useState<Knowledge[]>([]);

  const { getAllKnowledge } = useKnowledgeApi();
  const { data: brainKnowledges, isLoading: isPending } = useQuery({
    queryKey: [getKnowledgeDataKey(brainId)],
    queryFn: () => getAllKnowledge({ brainId }),
  });

  useEffect(() => {
    if (brainKnowledges === undefined) {
      return;
    }
    setAllKnowledge(brainKnowledges);
  }, [brainKnowledges]);

  return {
    isPending,
    allKnowledge,
    setAllKnowledge,
  };
};
