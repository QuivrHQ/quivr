/* eslint-disable */
import { useEffect, useState } from "react";

import { useAxios } from "@/lib/hooks";

import { useEventTracking } from "@/services/analytics/useEventTracking";
import { useTranslation } from "react-i18next";
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
  const { t } = useTranslation(["translation", "explore"]);

  const [documents, setDocuments] = useState<DocumentDetails[]>([]);
  const [loading, setLoading] = useState<Boolean>(false);

  if (!session) {
    throw new Error(t("sessionNotFound", { ns: "explore" }));
  }

  useEffect(() => {
    const fetchDocuments = async () => {
      setLoading(true);
      void track("GET_DOCUMENT_DETAILS");
      try {
        const res = await axiosInstance.get<{ documents: DocumentDetails[] }>(
          `/explore/${documentName}/`
        );
        setDocuments(res.data.documents);
      } catch (error) {
        setDocuments([]);
        console.error(error);
      }
      setLoading(false);
    };
    fetchDocuments();
  }, [axiosInstance, documentName]);

  function Data() {
    return (
      <div className="prose dark:prose-invert">
        <h1
          data-testid="document-name"
          className="text-bold text-3xl break-words"
        >
          {documentName}
        </h1>
        {documents.length > 0 ? (
          <>
            <p>
              {t("chunkNumber", { quantity: documents.length, ns: "explore" })}
            </p>
            <div className="flex flex-col">
              {Object.entries(documents[0]).map(([key, value]) => {
                if (value && typeof value === "object") return;
                return (
                  <div className="grid grid-cols-2 py-2 border-b" key={key}>
                    <p className="capitalize font-bold break-words">
                      {key.replaceAll("_", " ")}
                    </p>
                    <span className="break-words my-auto">
                      {String(value || t("notAvailable", { ns: "explore" }))}
                    </span>
                  </div>
                );
              })}
            </div>
          </>
        ) : (
          <p>{t("notAvailable", { ns: "explore" })}</p>
        )}
      </div>
    );
  }

  if (loading) {
    return <div>{t("loading")}</div>;
  } else {
    return <Data />;
  }
};

export default DocumentData;
