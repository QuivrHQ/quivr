import { useEffect, useState } from "react";

import { useKnowledgeContext } from "@/app/knowledge/KnowledgeProvider/hooks/useKnowledgeContext";
import { KMSElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import ProviderAccount from "./ProviderAccount/ProviderAccount";
import styles from "./ProviderCurrentFolder.module.scss";

import CurrentFolderExplorerLine from "../../shared/CurrentFolderExplorerLine/CurrentFolderExplorerLine";
import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const ProviderCurrentFolder = (): JSX.Element => {
  const [providerRootElements, setproviderRootElements] =
    useState<KMSElement[]>();
  const [loading, setLoading] = useState(false);
  const { exploredProvider, currentFolder, exploredSpecificAccount } =
    useKnowledgeContext();
  const { getSyncFiles } = useSync();

  const fetchCurrentFolderElements = () => {
    setLoading(true);
    void (async () => {
      try {
        const res = await getSyncFiles(
          exploredProvider?.syncs[0].id ?? 0,
          currentFolder?.sync_file_id ?? undefined
        );
        setproviderRootElements(res);
        setLoading(false);
      } catch (error) {
        console.error("Failed to get sync files:", error);
      }
    })();
  };

  useEffect(() => {
    if (exploredProvider && exploredProvider.syncs.length === 1) {
      void fetchCurrentFolderElements();
    }
  }, [currentFolder, exploredProvider]);

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
          <div className={styles.current_folder_content}>
            {providerRootElements?.map((element, index) => (
              <CurrentFolderExplorerLine
                key={index}
                element={{
                  ...element,
                  parentKMSElement: currentFolder,
                }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProviderCurrentFolder;
