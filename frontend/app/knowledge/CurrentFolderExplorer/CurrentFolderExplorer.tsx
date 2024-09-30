import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { KMSElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./CurrentFolderExplorer.module.scss";
import CurrentFolderExplorerLine from "./CurrentFolderExplorerLine/CurrentFolderExplorerLine";

import { useKnowledgeContext } from "../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const [loading, setLoading] = useState(false);
  const [syncElements, setKMSElements] = useState<KMSElement[]>();
  const { currentFolder, setCurrentFolder, quivrRootSelected } =
    useKnowledgeContext();
  const { getSyncFiles } = useSync();
  const { getFiles } = useKnowledgeApi();

  const fetchSyncFiles = async (folderId: string) => {
    setLoading(true);
    if (currentFolder?.sync_id) {
      try {
        const res = await getSyncFiles(currentFolder.sync_id, folderId);
        setKMSElements(res);
      } catch (error) {
        console.error("Failed to get sync files:", error);
      } finally {
        setLoading(false);
      }
    }
  };

  const fetchQuivrFiles = async () => {
    try {
      const res = await getFiles(null);
      setKMSElements(res);
    } catch (error) {
      console.error("Failed to get files:", error);
    }
  };

  useEffect(() => {
    if (currentFolder?.sync_id && currentFolder.sync_file_id) {
      void fetchSyncFiles(currentFolder.sync_file_id);
    } else if (quivrRootSelected) {
      void fetchQuivrFiles();
    }
  }, [currentFolder]);

  const loadParentFolder = () => {
    if (currentFolder?.parentKMSElement) {
      setCurrentFolder({
        ...currentFolder.parentKMSElement,
        parentKMSElement: currentFolder.parentKMSElement.parentKMSElement,
      });
    }
  };

  return (
    <div className={styles.current_folder_explorer_container}>
      <div className={styles.current_folder_explorer_wrapper}>
        <div className={styles.header}>
          {currentFolder?.parentKMSElement && (
            <div className={styles.parent_folder}>
              {currentFolder.parentKMSElement.icon && (
                <div className={styles.icon}>
                  {currentFolder.parentKMSElement.icon}
                </div>
              )}
              <span
                className={styles.name}
                onClick={() => void loadParentFolder()}
              >
                {currentFolder.parentKMSElement.file_name?.replace(
                  /(\..+)$/,
                  ""
                )}
              </span>
              <Icon name="chevronRight" size="normal" color="black" />
            </div>
          )}
          <div className={styles.current_folder}>
            {currentFolder?.icon && (
              <div className={styles.icon}>{currentFolder.icon}</div>
            )}
            <span
              className={`${styles.name} ${
                currentFolder?.parentKMSElement ? styles.selected : ""
              }`}
            >
              {currentFolder?.file_name?.replace(/(\..+)$/, "")}
            </span>
          </div>
        </div>
        <div className={styles.current_folder_content}>
          {loading ? (
            <div className={styles.loading_icon}>
              <LoaderIcon size="large" color="primary" />
            </div>
          ) : (
            syncElements
              ?.sort((a, b) => Number(b.is_folder) - Number(a.is_folder))
              .map((syncElement, index) => (
                <div key={index}>
                  <CurrentFolderExplorerLine element={syncElement} />
                </div>
              ))
          )}
        </div>
      </div>
    </div>
  );
};

export default CurrentFolderExplorer;
