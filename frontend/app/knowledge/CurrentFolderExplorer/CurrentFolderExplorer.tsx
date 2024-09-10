import styles from "./CurrentFolderExplorer.module.scss";

import { useKnowledgeContext } from "../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const { currentFolder } = useKnowledgeContext();

  return (
    <div className={styles.current_folder_explorer_wrapper}>
      <div className={styles.header}>
        <span>{currentFolder?.name}</span>
      </div>
    </div>
  );
};

export default CurrentFolderExplorer;
