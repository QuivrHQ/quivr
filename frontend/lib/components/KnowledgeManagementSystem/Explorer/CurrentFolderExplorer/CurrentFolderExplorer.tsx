import { useEffect } from "react";

import styles from "./CurrentFolderExplorer.module.scss";
import ProviderCurrentFolder from "./ProviderCurrentFolder/ProviderCurrentFolder";
import QuivrCurrentFolder from "./QuivrCurrentFolder/QuivrCurrentFolder";
import SyncCurrentFolder from "./SyncCurrentFolder/SyncCurrentFolder";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const { exploringQuivr, exploredProvider, setExploringQuivr } =
    useKnowledgeContext();

  useEffect(() => {
    setExploringQuivr(true);
  }, []);

  useEffect(() => {
    console.info(exploredProvider);
  }, [exploredProvider]);

  return (
    <div className={styles.current_folder_explorer_container}>
      {exploredProvider ? (
        <ProviderCurrentFolder />
      ) : exploringQuivr ? (
        <QuivrCurrentFolder />
      ) : (
        <SyncCurrentFolder />
      )}
    </div>
  );
};

export default CurrentFolderExplorer;
