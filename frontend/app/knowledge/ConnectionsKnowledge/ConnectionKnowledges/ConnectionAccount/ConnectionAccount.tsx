import { useEffect, useState } from "react";

import { Sync, SyncElements } from "@/lib/api/sync/types"; // Assurez-vous que SyncElement est bien importé
import { useSync } from "@/lib/api/sync/useSync";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionAccount.module.scss";

import SyncFolder from "../SyncFolder/SyncFolder";

interface ConnectionAccountProps {
  sync: Sync;
  index: number;
}

const ConnectionAccount = ({
  sync,
  index,
}: ConnectionAccountProps): JSX.Element => {
  const { getSyncFiles } = useSync();
  const [syncElements, setSyncElements] = useState<SyncElements>();
  const [folded, setFolded] = useState(true);

  useEffect(() => {
    void (async () => {
      try {
        const res = await getSyncFiles(sync.id);
        console.info(res);
        setSyncElements(res);
      } catch (error) {
        console.error("Failed to get sync files:", error);
      }
    })();
  }, [sync.id]);

  return (
    <div className={styles.account_section_wrapper}>
      <div className={styles.account_line_wrapper}>
        <Icon
          name={folded ? "chevronRight" : "chevronDown"}
          size="normal"
          color="black"
          handleHover={true}
          onClick={() => setFolded(!folded)}
        />
        <ConnectionIcon letter={sync.email[0]} index={index} />
        <span>{sync.email}</span>
      </div>
      {!folded && (
        <div className={styles.sync_elements_wrapper}>
          {syncElements?.files
            .filter((file) => file.is_folder)
            .map((element, id) => (
              <div key={id}>
                <SyncFolder element={element} indent={2} />
              </div>
            ))}
        </div>
      )}
    </div>
  );
};

export default ConnectionAccount;
