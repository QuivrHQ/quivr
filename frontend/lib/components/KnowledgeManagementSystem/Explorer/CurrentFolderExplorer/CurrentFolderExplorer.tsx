import { useEffect } from "react";

import styles from "./CurrentFolderExplorer.module.scss";
import ProviderCurrentFolder from "./ProviderCurrentFolder/ProviderCurrentFolder";
import QuivrCurrentFolder from "./QuivrCurrentFolder/QuivrCurrentFolder";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";

interface CurrentFolderExplorerProps {
  fromBrainStudio?: boolean;
}

const CurrentFolderExplorer = ({
  fromBrainStudio,
}: CurrentFolderExplorerProps): JSX.Element => {
  const { exploringQuivr, exploredProvider, setExploringQuivr } =
    useKnowledgeContext();

  useEffect(() => {
    setExploringQuivr(true);
  }, []);

  return (
    <div className={styles.current_folder_explorer_container}>
      {exploredProvider || !exploringQuivr ? (
        <ProviderCurrentFolder fromBrainStudio={fromBrainStudio} />
      ) : (
        <QuivrCurrentFolder fromBrainStudio={fromBrainStudio} />
      )}
    </div>
  );
};

export default CurrentFolderExplorer;
