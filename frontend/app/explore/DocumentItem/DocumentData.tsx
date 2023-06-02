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
    <div className="prose">
      <p>No. of documents: {documents.length}</p>
      {/* {documents.map((doc) => (
        <pre key={doc.name}>{JSON.stringify(doc)}</pre>
      ))} */}
      <div className="flex flex-col gap-2">
        {documents[0] &&
          Object.keys(documents[0]).map((k) => {
            return (
              <div className="grid grid-cols-2 border-b py-2" key={k}>
                <span className="capitalize font-bold">
                  {k.replaceAll("_", " ")}
                </span>
                <span className="">{documents[0][k] || "Not Available"}</span>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default DocumentData;
