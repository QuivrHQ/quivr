/* eslint-disable */
import { useEffect, useState } from "react";

import { useAxios } from "@/lib/hooks";

import { useEventTracking } from "@/services/analytics/useEventTracking";
import { useSupabase } from "../../../lib/context/SupabaseProvider";

interface DocumentDataProps {
  documentName: string;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type DocumentDetails = any;
//TODO: review this component logic, types and purposes

const DocumentData = ({ documentName }: DocumentDataProps): JSX.Element => {
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();
  const { track } = useEventTracking();

  const [documents, setDocuments] = useState<DocumentDetails[]>([]);

  if (!session) {
    throw new Error("User session not found");
  }

  useEffect(() => {
    const fetchDocuments = async () => {
      void track("GET_DOCUMENT_DETAILS");
      const res = await axiosInstance.get<{ documents: DocumentDetails[] }>(
        `/explore/${documentName}/`
      );
      setDocuments(res.data.documents);
    };
    fetchDocuments();
  }, [axiosInstance, documentName]);

  return (
    <div className="prose dark:prose-invert">
      <h1 className="text-bold text-3xl break-words">{documentName}</h1>
      <p>No. of chunks: {documents.length}</p>

      <div className="flex flex-col">
        {documents[0] &&
          Object.entries(documents[0]).map(([key, value]) => {
            if (value && typeof value === "object") return;
            return (
              <div className="grid grid-cols-2 py-2 border-b" key={key}>
                <p className="capitalize font-bold break-words">
                  {key.replaceAll("_", " ")}
                </p>
                <span className="break-words my-auto">
                  {String(value || "Not Available")}
                </span>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default DocumentData;
