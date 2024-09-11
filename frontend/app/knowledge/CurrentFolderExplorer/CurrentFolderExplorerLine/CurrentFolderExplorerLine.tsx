import { SyncElement } from "@/lib/api/sync/types";

import styles from "./CurrentFolderExplorerLine.module.scss";

interface CurrentFolderExplorerLineProps {
  element: SyncElement;
}

const SyncFolder = ({
  element,
}: CurrentFolderExplorerLineProps): JSX.Element => {
  return (
    <div className={styles.folder_explorer_line_wrapper}>{element.name}</div>
  );
};

export default SyncFolder;
