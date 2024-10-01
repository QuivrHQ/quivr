import styles from "./ProviderCurrentFolder.module.scss";

import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const ProviderCurrentFolder = (): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <FolderExplorerHeader />
      <div className={styles.current_folder_content}>PROVIDER</div>
    </div>
  );
};

export default ProviderCurrentFolder;
