"use client";

import axios from "axios";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { useNotesEditorContext } from "@/lib/context/NotesEditorProvider/hooks/useNotesEditorContext";
import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";

import styles from "./KnowledgeItem.module.scss";

type KnowledgeItemProps = {
  knowledge: Knowledge;
};

const KnowledgeItem = ({ knowledge }: KnowledgeItemProps): JSX.Element => {
  const { generateSignedUrlKnowledge } = useKnowledgeApi();
  const { updateContent } = useNotesEditorContext();

  const logFileContent = async () => {
    if (isUploadedKnowledge(knowledge)) {
      let download_url = await generateSignedUrlKnowledge({
        knowledgeId: knowledge.id,
      });
      download_url = download_url.replace("host.docker.internal", "localhost");

      try {
        const response = await axios.get(download_url, {
          responseType: "blob",
        });

        const reader = new FileReader();

        reader.onload = (event) => {
          const text = event.target?.result as string;
          const html = text.replace(/\n/g, "<br/>");
          updateContent(html);
        };

        reader.onerror = (event) => {
          console.error("Error reading file:", event);
        };

        reader.readAsText(new Blob([response.data]));
      } catch (error) {
        console.error("Error downloading the file:", error);
      }
    }
  };

  return (
    <div className={styles.knowledge_item_wrapper}>
      {isUploadedKnowledge(knowledge) ? (
        <span className={styles.name} onClick={() => void logFileContent()}>
          {knowledge.fileName}
        </span>
      ) : (
        <a
          className={styles.name}
          href={knowledge.url}
          target="_blank"
          rel="noopener noreferrer"
        >
          {knowledge.url}
        </a>
      )}
    </div>
  );
};

export default KnowledgeItem;
