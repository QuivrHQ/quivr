import { useSupabase } from "@/app/supabase-provider";
import { useAxios } from "@/lib/useAxios";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { Document } from "../types";

export default function useDocuments() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isPending, setIsPending] = useState(true);
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();

  if (session === null) {
    redirect("/login");
  }

  useEffect(() => {
    const fetchDocuments = async () => {
      setIsPending(true);
      try {
        console.log(
          `Fetching documents from ${process.env.NEXT_PUBLIC_BACKEND_URL}/explore`
        );
        const response = await axiosInstance.get<{ documents: Document[] }>(
          "/explore"
        );
        setDocuments(response.data.documents);
      } catch (error) {
        console.error("Error fetching documents", error);
        setDocuments([]);
      }
      setIsPending(false);
    };
    fetchDocuments();
  }, [session.access_token, axiosInstance]);

  return {
    isPending,
    documents,
    setDocuments,
  };
}
