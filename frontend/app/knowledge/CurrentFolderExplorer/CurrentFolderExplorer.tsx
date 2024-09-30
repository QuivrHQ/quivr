import { useEffect, useState } from "react";

import { SyncElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./CurrentFolderExplorer.module.scss";
import CurrentFolderExplorerLine from "./CurrentFolderExplorerLine/CurrentFolderExplorerLine";

import { useKnowledgeContext } from "../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const [loading, setLoading] = useState(false);
  const [syncElements, setSyncElements] = useState<SyncElement[]>();
  const { currentFolder, setCurrentFolder } = useKnowledgeContext();
  const { getSyncFiles } = useSync();

  const fetchSyncFiles = async (folderId: string) => {
    setLoading(true);
    if (currentFolder) {
      try {
        const res = await getSyncFiles(currentFolder.sync_id, folderId);
        setSyncElements(res);
      } catch (error) {
        console.error("Failed to get sync files:", error);
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    if (currentFolder?.sync_id && currentFolder.sync_file_id) {
      void fetchSyncFiles(currentFolder.sync_file_id);
    }
  }, [currentFolder]);

  const loadParentFolder = () => {
    if (currentFolder?.parentSyncElement) {
      setCurrentFolder({
        ...currentFolder.parentSyncElement,
        parentSyncElement: currentFolder.parentSyncElement.parentSyncElement,
      });
    }
  };

  return (
    <div className={styles.current_folder_explorer_container}>
      <div className={styles.current_folder_explorer_wrapper}>
        <div className={styles.header}>
          {currentFolder?.parentSyncElement && (
            <div className={styles.parent_folder}>
              {currentFolder.parentSyncElement.icon && (
                <div className={styles.icon}>
                  {currentFolder.parentSyncElement.icon}
                </div>
              )}
              <span
                className={styles.name}
                onClick={() => void loadParentFolder()}
              >
                {currentFolder.parentSyncElement.file_name?.replace(
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
                currentFolder?.parentSyncElement ? styles.selected : ""
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
