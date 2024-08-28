import { useEffect, useState } from "react";

import { Sync, SyncElements } from "@/lib/api/sync/types"; // Assurez-vous que SyncElement est bien importé
import { useSync } from "@/lib/api/sync/useSync";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionAccount.module.scss";

import SyncFile from "../SyncFile/SyncFile";
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
    console.info("Getting sync files...");
    void (async () => {
      try {
        const res = await getSyncFiles(sync.id);
        console.info(res);
        setSyncElements(res); // Supposons que res est déjà un tableau de SyncElement
      } catch (error) {
        console.error("Failed to get sync files:", error);
      }
    })();
  }, [sync.id]);

  return (
    <div>
      <div className={styles.account_line_wrapper}>
        <Icon
          name="chevronRight"
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
          {syncElements?.files.map((element, id) => (
            <div key={id}>
              {element.is_folder ? (
                <SyncFolder element={element} indent={2} />
              ) : (
                <SyncFile element={element} />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ConnectionAccount;
