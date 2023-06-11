import { useSupabase } from "@/app/supabase-provider";
import { useAxios } from "@/lib/useAxios";
import { useEffect, useState } from "react";
import { DocumentData } from "../../types";

export default function useDocumentData(name: string) {
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();

  const [documents, setDocuments] = useState<DocumentData[]>([]);

  if (!session) {
    throw new Error("User session not found");
  }

  useEffect(() => {
    const fetchDocuments = async () => {
      const res = await axiosInstance.get<{ documents: DocumentData[] }>(
        `/explore/${name}`
      );
      setDocuments(res.data.documents);
    };
    fetchDocuments();
  }, [axiosInstance, name]);

  return { documents };
}
