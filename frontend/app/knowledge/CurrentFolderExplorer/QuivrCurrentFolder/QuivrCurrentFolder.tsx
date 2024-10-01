import { UUID } from "crypto";
import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { KMSElement } from "@/lib/api/sync/types";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./QuivrCurrentFolder.module.scss";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";
import CurrentFolderExplorerLine from "../../shared/CurrentFolderExplorerLine/CurrentFolderExplorerLine";
import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const QuivrCurrentFolder = (): JSX.Element => {
  const [loading, setLoading] = useState(false);
  const [quivrElements, setQuivrElements] = useState<KMSElement[]>();
  const { currentFolder } = useKnowledgeContext();
  const { getFiles } = useKnowledgeApi();

  const fetchQuivrFiles = async (folderId: UUID | null) => {
    setLoading(true);
    try {
      const res = await getFiles(folderId);
      setQuivrElements(res);
    } catch (error) {
      console.error("Failed to get sync files:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.info("hey");
    void fetchQuivrFiles(currentFolder?.id ?? null);
  }, [currentFolder]);

  return (
    <div className={styles.main_container}>
      <FolderExplorerHeader />
      <div className={styles.current_folder_content}>
        {loading ? (
          <div className={styles.loading_icon}>
            <LoaderIcon size="large" color="primary" />
          </div>
        ) : (
          quivrElements
            ?.sort((a, b) => Number(b.is_folder) - Number(a.is_folder))
            .map((element, index) => (
              <div key={index}>
                <CurrentFolderExplorerLine
                  element={{
                    ...element,
                    parentKMSElement: currentFolder,
                  }}
                />
              </div>
            ))
        )}
      </div>
    </div>
  );
};

export default QuivrCurrentFolder;
