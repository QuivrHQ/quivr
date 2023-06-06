import { useAxios } from "@/lib/useAxios";
import { useEffect, useState } from "react";
import { useSupabase } from "../../supabase-provider";

interface DocumentDataProps {
  documentName: string;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type DocumentDetails = any;
//TODO: review this component logic, types and purposes

const DocumentData = ({ documentName }: DocumentDataProps): JSX.Element => {
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();

  const [documents, setDocuments] = useState<DocumentDetails[]>([]);

  if (!session) {
    throw new Error("User session not found");
  }

  useEffect(() => {
    const fetchDocuments = async () => {
      const res = await axiosInstance.get<{ documents: DocumentDetails[] }>(
        `/explore/${documentName}`
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
          Object.keys(documents[0]).map((doc) => {
            return (
              <div className="grid grid-cols-2 py-2 border-b" key={doc}>
                <p className="capitalize font-bold break-words">
                  {doc.replaceAll("_", " ")}
                </p>
                <span className="break-words my-auto">
                  {documents[0][doc] || "Not Available"}
                </span>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default DocumentData;
