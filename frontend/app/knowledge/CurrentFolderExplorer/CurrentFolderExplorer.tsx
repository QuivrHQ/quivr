import styles from "./CurrentFolderExplorer.module.scss";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { useKnowledgeContext } from "../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const { currentFolder } = useKnowledgeContext();

  return (
    <div className={styles.current_folder_explorer_container}>
      <div className={styles.current_folder_explorer_wrapper}>
        <div className={styles.header}>
          <Icon name="folder" size="large" color="black" />
          <span>{currentFolder?.name}</span>
        </div>
      </div>
    </div>
  );
};

export default CurrentFolderExplorer;
