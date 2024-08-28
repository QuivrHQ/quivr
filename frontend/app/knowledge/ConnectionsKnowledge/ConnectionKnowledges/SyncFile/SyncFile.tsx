import { SyncElement } from "@/lib/api/sync/types";

import styles from "./SyncFile.module.scss";

interface SyncFileProps {
  element: SyncElement;
}

const SyncFile = ({ element }: SyncFileProps): JSX.Element => {
  console.info(element);

  return <div className={styles.file_wrapper}></div>;
};

export default SyncFile;
