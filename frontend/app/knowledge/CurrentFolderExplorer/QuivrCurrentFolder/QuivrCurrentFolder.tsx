import styles from "./QuivrCurrentFolder.module.scss";

import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const QuivrCurrentFolder = (): JSX.Element => {
  return (
    <div className={styles.main_container}>
      <FolderExplorerHeader />
    </div>
  );
};

export default QuivrCurrentFolder;
