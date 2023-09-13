import { useQuery } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useEffect, useState } from "react";

import { getBrainKnowledgeDataKey } from "@/lib/api/brain/config";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { Document } from "@/lib/types/Document";

type useKnowledgeTabProps = {
  brainId: UUID;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeTab = ({ brainId }: useKnowledgeTabProps) => {
  const [documents, setDocuments] = useState<Document[]>([]);

  const { getBrainDocuments } = useBrainApi();
  const { data: brainDocuments, isLoading: isPending } = useQuery({
    queryKey: [getBrainKnowledgeDataKey(brainId)],
    queryFn: () => getBrainDocuments(brainId),
  });

  useEffect(() => {
    if (brainDocuments === undefined) {
      return;
    }
    setDocuments(brainDocuments);
  }, [brainDocuments]);

  return {
    isPending,
    documents,
    setDocuments,
  };
};
