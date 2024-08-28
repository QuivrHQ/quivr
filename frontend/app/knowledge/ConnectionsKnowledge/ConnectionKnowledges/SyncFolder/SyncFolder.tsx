import { SyncElement } from "@/lib/api/sync/types";

import styles from "./SyncFolder.module.scss";

interface SyncFolderProps {
  element: SyncElement;
  indent: number;
}

const SyncFolder = ({ element, indent }: SyncFolderProps): JSX.Element => {
  const paddingLeft = `${28 * indent}px`;

  return (
    <div className={styles.folder_wrapper} style={{ paddingLeft }}>
      {element.name}
    </div>
  );
};

export default SyncFolder;
