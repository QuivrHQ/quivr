import { useEffect } from "react";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useCustomDropzone } from "@/lib/hooks/useDropzone";

import styles from "./FromDocuments.module.scss";

export const FromDocuments = (): JSX.Element => {
  const { getRootProps, getInputProps, open } = useCustomDropzone();
  const { knowledgeToFeed } = useKnowledgeToFeedContext();

  useEffect(() => {
    console.info(knowledgeToFeed);
  }, [knowledgeToFeed]);

  return (
    <div className={styles.from_document_wrapper} {...getRootProps()}>
      <div className={styles.input} onClick={open}>
        <span>Drag androp or click here to browse files </span>
        <input {...getInputProps()} />
      </div>
    </div>
  );
};
