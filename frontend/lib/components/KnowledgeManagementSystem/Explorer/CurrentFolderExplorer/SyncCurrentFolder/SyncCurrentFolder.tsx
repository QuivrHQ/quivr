import { useEffect, useState } from "react";

import { KMSElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./SyncCurrentFolder.module.scss";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useKnowledgeContext } from "../../../KnowledgeProvider/hooks/useKnowledgeContext";
import CurrentFolderExplorerLine from "../../shared/CurrentFolderExplorerLine/CurrentFolderExplorerLine";
import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const SyncCurrentFolder = (): JSX.Element => {
  const [loading, setLoading] = useState(false);
  const [syncElements, setKMSElements] = useState<KMSElement[]>();
  const [showAddToBrainsModal, setShowAddToBrainsModal] =
    useState<boolean>(false);
  const { currentFolder } = useKnowledgeContext();
  const { getSyncFiles } = useSync();

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

  useEffect(() => {
    if (currentFolder?.sync_id && currentFolder.sync_file_id) {
      void fetchSyncFiles(currentFolder.sync_file_id);
    }
  }, [currentFolder]);

  return (
    <div className={styles.current_folder_explorer_wrapper}>
      <FolderExplorerHeader />
      <div className={styles.current_folder_content}>
        {loading ? (
          <div className={styles.loading_icon}>
            <LoaderIcon size="large" color="primary" />
          </div>
        ) : (
          <>
            <div className={styles.content_header}>
              aaaa
              <QuivrButton
                iconName="sync"
                label="Connect to brains"
                color="primary"
                onClick={() => setShowAddToBrainsModal(true)}
                small={true}
                // disabled={!selectedKnowledges.length}
              />
            </div>
            {syncElements
              ?.sort((a, b) => Number(b.is_folder) - Number(a.is_folder))
              .map((syncElement, index) => (
                <div key={index}>
                  <CurrentFolderExplorerLine
                    element={{
                      ...syncElement,
                      parentKMSElement: currentFolder,
                    }}
                  />
                </div>
              ))}
          </>
        )}
      </div>
    </div>
  );
};

export default SyncCurrentFolder;
