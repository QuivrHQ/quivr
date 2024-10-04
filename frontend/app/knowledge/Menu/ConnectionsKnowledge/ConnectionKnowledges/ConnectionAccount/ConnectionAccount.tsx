import { useEffect, useState } from "react";

import { KMSElement, Sync, SyncsByProvider } from "@/lib/api/sync/types"; // Assurez-vous que KMSElement est bien importé
import { useSync } from "@/lib/api/sync/useSync";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./ConnectionAccount.module.scss";

import SyncFolder from "../SyncFolder/SyncFolder";

interface ConnectionAccountProps {
  sync: Sync;
  index: number;
  singleAccount?: boolean;
  providerGroup?: SyncsByProvider;
}

const ConnectionAccount = ({
  sync,
  index,
  singleAccount,
  providerGroup,
}: ConnectionAccountProps): JSX.Element => {
  const { getSyncFiles } = useSync();
  const [loading, setLoading] = useState(false);
  const [syncElements, setKMSElements] = useState<KMSElement[]>();
  const [folded, setFolded] = useState(true);

  const getFiles = () => {
    setLoading(true);
    void (async () => {
      try {
        const res = await getSyncFiles(sync.id);
        setKMSElements(res);
        setLoading(false);
      } catch (error) {
        console.error("Failed to get sync files:", error);
      }
    })();
  };

  useEffect(() => {
    getFiles();
  }, []);

  useEffect(() => {
    if (singleAccount) {
      getFiles();
    }
  }, []);

  return (
    <div className={styles.account_section_wrapper}>
      {!singleAccount && (
        <div className={styles.account_line_wrapper}>
          <Icon
            name={folded ? "chevronRight" : "chevronDown"}
            size="normal"
            color="dark-grey"
            handleHover={true}
            onClick={() => setFolded(!folded)}
          />
          <div className={styles.hoverable}>
            <ConnectionIcon letter={sync.email[0]} index={index} />
            <span className={styles.name}>{sync.email}</span>
          </div>
        </div>
      )}
      {(!singleAccount && !folded) || singleAccount ? (
        loading ? (
          <div className={styles.loader_icon}>
            <LoaderIcon color="primary" size="small" />
          </div>
        ) : (
          <div
            className={`${styles.sync_elements_wrapper} ${
              !syncElements?.filter((file) => file.is_folder).length
                ? styles.empty
                : ""
            } ${singleAccount ? styles.single_account : ""}`}
          >
            {syncElements
              ?.filter((file) => file.is_folder)
              .map((element, id) => (
                <div key={id}>
                  <SyncFolder
                    element={{
                      ...element,
                      fromProvider: providerGroup,
                    }}
                  />
                </div>
              ))}
          </div>
        )
      ) : null}
    </div>
  );
};

export default ConnectionAccount;
