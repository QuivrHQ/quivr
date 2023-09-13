import { UUID } from "crypto";
import { useEffect, useState } from "react";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useAxios } from "@/lib/hooks";
import { Document } from "@/lib/types/Document";

type useKnowledgeTabProps = {
  brainId: UUID;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeTab = ({ brainId }: useKnowledgeTabProps) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isPending, setIsPending] = useState(true);
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();

  const { getBrainDocuments } = useBrainApi();

  useEffect(() => {
    const fetchDocuments = async () => {
      setIsPending(true);
      try {
        const brainDocuments = await getBrainDocuments(brainId);
        setDocuments(brainDocuments);
      } catch (error) {
        console.error("Error fetching documents", error);
        setDocuments([]);
      }
      setIsPending(false);
    };
    void fetchDocuments();
  }, [session?.access_token, axiosInstance]);

  return {
    isPending,
    documents,
    setDocuments,
  };
};
