import { useEffect, useState } from "react";

import { SyncElements } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./CurrentFolderExplorer.module.scss";
import CurrentFolderExplorerLine from "./CurrentFolderExplorerLine/CurrentFolderExplorerLine";

import { useKnowledgeContext } from "../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const [loading, setLoading] = useState(false);
  const [syncElements, setSyncElements] = useState<SyncElements>();
  const { currentFolder, setCurrentFolder } = useKnowledgeContext();
  const { getSyncFiles } = useSync();

  const fetchSyncFiles = async (folderId: string) => {
    setLoading(true);
    if (currentFolder) {
      try {
        const res = await getSyncFiles(currentFolder.syncId, folderId);
        setSyncElements((prevState) => ({
          ...prevState,
          files: res.files.map((syncElement) => ({
            ...syncElement,
            syncId: currentFolder.syncId,
            parentSyncElement: currentFolder,
          })),
        }));
      } catch (error) {
        console.error("Failed to get sync files:", error);
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    if (currentFolder?.syncId && currentFolder.id) {
      void fetchSyncFiles(currentFolder.id);
    }
  }, [currentFolder]);

  const loadParentFolder = () => {
    if (currentFolder?.parentSyncElement) {
      console.info(currentFolder.parentSyncElement);
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
                {currentFolder.parentSyncElement.name?.replace(/(\..+)$/, "")}
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
              {currentFolder?.name?.replace(/(\..+)$/, "")}
            </span>
          </div>
        </div>
        <div className={styles.current_folder_content}>
          {loading ? (
            <div className={styles.loading_icon}>
              <LoaderIcon size="large" color="primary" />
            </div>
          ) : (
            syncElements?.files
              .sort((a, b) => Number(b.is_folder) - Number(a.is_folder))
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
