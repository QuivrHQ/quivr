import { useEffect } from "react";

import { useKnowledgeContext } from "@/app/knowledge/KnowledgeProvider/hooks/useKnowledgeContext";

import styles from "./ProviderCurrentFolder.module.scss";

import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const ProviderCurrentFolder = (): JSX.Element => {
  const { providerRootSelected } = useKnowledgeContext();

  useEffect(() => {
    console.info(providerRootSelected);
  }, [providerRootSelected]);

  return (
    <div className={styles.main_container}>
      <FolderExplorerHeader />
      <div className={styles.current_folder_content}>
        {providerRootSelected?.syncs &&
        providerRootSelected.syncs.length > 1 ? (
          providerRootSelected.syncs.map((sync, index) => (
            <div key={index}>{sync.email}</div>
          ))
        ) : (
          <div>hey</div>
        )}
      </div>
    </div>
  );
};

export default ProviderCurrentFolder;
