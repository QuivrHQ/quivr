import { useSync } from "@/lib/api/sync/useSync";

import styles from "./ConnectionCards.module.scss";
import { ConnectionSection } from "./ConnectionSection/ConnectionSection";

export const ConnectionCards = (): JSX.Element => {
  const { syncGoogleDrive, syncSharepoint } = useSync();

  return (
    <div className={styles.connection_cards}>
      <ConnectionSection
        label="Google Drive"
        provider="Google"
        callback={(name) => syncGoogleDrive(name)}
      />
      <ConnectionSection
        label="Sharepoint"
        provider="Azure"
        callback={(name) => syncSharepoint(name)}
      />
    </div>
  );
};
