import { UUID } from "crypto";
import { useEffect, useState } from "react";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useAxios } from "@/lib/hooks";
import { Document } from "@/lib/types/Document";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useExplore = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isPending, setIsPending] = useState(true);
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();
  const { currentBrainId } = useBrainContext();
  const { getBrainDocuments } = useBrainApi();

  useEffect(() => {
    const fetchDocuments = async (brainId: UUID | null) => {
      setIsPending(true);
      try {
        if (brainId === null) {
          throw new Error("Brain id not found");
        }
        const brainDocuments = await getBrainDocuments(brainId);
        setDocuments(brainDocuments);
      } catch (error) {
        console.error("Error fetching documents", error);
        setDocuments([]);
      }
      setIsPending(false);
    };
    void fetchDocuments(currentBrainId);
  }, [session?.access_token, axiosInstance, currentBrainId]);

  return {
    isPending,
    documents,
    setDocuments,
  };
};
