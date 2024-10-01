import { useEffect } from "react";

import styles from "./CurrentFolderExplorer.module.scss";
import SyncCurrentFolder from "./SyncCurrentFolder/SyncCurrentFolder";

import { useKnowledgeContext } from "../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const { quivrRootSelected } = useKnowledgeContext();

  useEffect(() => {
    console.info(quivrRootSelected);
  }, [quivrRootSelected]);

  return (
    <div className={styles.current_folder_explorer_container}>
      {!quivrRootSelected ? <SyncCurrentFolder /> : <div> HAHA</div>}
    </div>
  );
};

export default CurrentFolderExplorer;
