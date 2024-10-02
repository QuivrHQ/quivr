import { useEffect } from "react";

import styles from "./CurrentFolderExplorer.module.scss";
import ProviderCurrentFolder from "./ProviderCurrentFolder/ProviderCurrentFolder";
import QuivrCurrentFolder from "./QuivrCurrentFolder/QuivrCurrentFolder";
import SyncCurrentFolder from "./SyncCurrentFolder/SyncCurrentFolder";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";

const CurrentFolderExplorer = (): JSX.Element => {
  const { exploringQuivr, providerRootSelected, setExploringQuivr } =
    useKnowledgeContext();

  useEffect(() => {
    setExploringQuivr(true);
  }, []);

  return (
    <div className={styles.current_folder_explorer_container}>
      {providerRootSelected ? (
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
