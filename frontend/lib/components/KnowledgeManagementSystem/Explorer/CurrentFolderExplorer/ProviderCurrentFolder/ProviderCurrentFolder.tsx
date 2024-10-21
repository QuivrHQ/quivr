import { useEffect, useState } from "react";

import { KMSElement, Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { useKnowledgeContext } from "@/lib/components/KnowledgeManagementSystem/KnowledgeProvider/hooks/useKnowledgeContext";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import ProviderAccount from "./ProviderAccount/ProviderAccount";
import styles from "./ProviderCurrentFolder.module.scss";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import AddToBrainsModal from "../../shared/CurrentFolderExplorerLine/ConnectedBrains/AddToBrainsModal/AddToBrainsModal";
import CurrentFolderExplorerLine from "../../shared/CurrentFolderExplorerLine/CurrentFolderExplorerLine";
import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const ProviderCurrentFolder = (): JSX.Element => {
  const [providerRootElements, setproviderRootElements] =
    useState<KMSElement[]>();
  const [loading, setLoading] = useState(false);
  const [showAddToBrainsModal, setShowAddToBrainsModal] =
    useState<boolean>(false);
  const {
    exploredProvider,
    currentFolder,
    exploredSpecificAccount,
    selectedKnowledges,
    setSelectedKnowledges,
  } = useKnowledgeContext();
  const { getSyncFiles } = useSync();

  const fetchCurrentFolderElements = (sync: Sync) => {
    setLoading(true);
    void (async () => {
      try {
        const res = await getSyncFiles(
          sync.id,
          currentFolder?.sync_file_id ?? undefined
        );
        setproviderRootElements(res);
        setLoading(false);
        setSelectedKnowledges([]);
      } catch (error) {
        console.error("Failed to get sync files:", error);
      }
    })();
  };

  useEffect(() => {
    if (exploredProvider) {
      if (exploredProvider.syncs.length === 1) {
        void fetchCurrentFolderElements(exploredProvider.syncs[0]);
      } else if (exploredSpecificAccount) {
        void fetchCurrentFolderElements(exploredSpecificAccount);
      }
    }
  }, [currentFolder, exploredProvider, exploredSpecificAccount]);

  return (
    <div className={styles.main_container}>
      <FolderExplorerHeader />
      <div className={styles.current_folder_content}>
        {exploredProvider?.syncs &&
        !exploredSpecificAccount &&
        exploredProvider.syncs.length > 1 ? (
          exploredProvider.syncs.map((sync, index) => (
            <div key={index}>
              <ProviderAccount sync={sync} index={index} />
            </div>
          ))
        ) : loading ? (
          <div className={styles.loading_icon}>
            <LoaderIcon color="primary" size="large" />
          </div>
        ) : (
          <>
            <div className={styles.content_header}>
              <QuivrButton
                iconName="sync"
                label="Connect to brains"
                color="primary"
                onClick={() => setShowAddToBrainsModal(true)}
                small={true}
                disabled={!selectedKnowledges.length}
              />
            </div>
            <div className={styles.current_folder_content}>
              {providerRootElements
                ?.sort((a, b) => Number(b.is_folder) - Number(a.is_folder))
                .map((element, index) => (
                  <CurrentFolderExplorerLine
                    key={index}
                    element={{
                      ...element,
                      parentKMSElement: currentFolder,
                    }}
                  />
                ))}
            </div>
          </>
        )}
      </div>
      {showAddToBrainsModal && (
        <div
          className={styles.modal_content}
          onClick={(e) => e.stopPropagation()}
        >
          <AddToBrainsModal
            isOpen={showAddToBrainsModal}
            setIsOpen={() => setShowAddToBrainsModal(false)}
            knowledges={selectedKnowledges}
          />
        </div>
      )}
    </div>
  );
};

export default ProviderCurrentFolder;
