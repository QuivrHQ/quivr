import { useKnowledgeContext } from "@/app/knowledge/KnowledgeProvider/hooks/useKnowledgeContext";

import styles from "./ProviderCurrentFolder.module.scss";

import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const ProviderCurrentFolder = (): JSX.Element => {
  const { providerRootSelected } = useKnowledgeContext();

  return (
    <div className={styles.main_container}>
      <FolderExplorerHeader />
      <div className={styles.current_folder_content}>
        {providerRootSelected?.syncs.map((sync) => sync.email)}
      </div>
    </div>
  );
};

export default ProviderCurrentFolder;
