import { useEffect, useState } from "react";

import { SyncElement, SyncElements } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./SyncFolder.module.scss";

interface SyncFolderProps {
  element: SyncElement;
  indent: number;
}

const SyncFolder = ({ element, indent }: SyncFolderProps): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const { getSyncFiles } = useSync();
  const [syncElements, setSyncElements] = useState<SyncElements>();
  const paddingLeft = `${16 * indent}px`;

  useEffect(() => {
    void (async () => {
      try {
        const res = await getSyncFiles(element.id);
        console.info(res);
        setSyncElements(res);
      } catch (error) {
        console.error("Failed to get sync files:", error);
      }
    })();
  }, [element.id]);

  return (
    <div className={styles.folder_wrapper} style={{ paddingLeft }}>
      <div className={styles.folder_line_wrapper}>
        <Icon
          name={folded ? "chevronRight" : "chevronDown"}
          size="normal"
          color="black"
          handleHover={true}
          onClick={() => setFolded(!folded)}
        />
        <span>{element.name}</span>
      </div>
      {!folded && (
        <div className={styles.sync_elements_wrapper}>
          {syncElements?.files
            .filter((file) => file.is_folder)
            .map((folder, id) => (
              <div key={id}>
                <SyncFolder element={folder} indent={indent + 1} />
              </div>
            ))}
        </div>
      )}
    </div>
  );
};

export default SyncFolder;
