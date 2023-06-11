import useDocumentData from "./hooks/useDocumentData";

interface DocumentDataProps {
  documentName: string;
}

const DocumentData = ({ documentName }: DocumentDataProps): JSX.Element => {
  const { documents } = useDocumentData(documentName);

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
