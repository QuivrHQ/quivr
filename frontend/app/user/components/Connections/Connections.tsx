import { useSync } from "@/lib/api/sync/useSync";

import { ConnectionSection } from "./ConnectionSection/ConnectionSection";
import styles from "./Connections.module.scss";

export const Connections = (): JSX.Element => {
  const { syncGoogleDrive, syncSharepoint, iconUrls } = useSync();

  return (
    <div className={styles.connections_wrapper}>
      <span className={styles.title}>Link apps you want to search across</span>
      <div className={styles.connection_cards}>
        <ConnectionSection
          label="Google Drive"
          iconUrl={iconUrls.Google}
          callback={(name) => syncGoogleDrive(name)}
        />
        <ConnectionSection
          label="Sharepoint"
          iconUrl={iconUrls.Azure}
          callback={(name) => syncSharepoint(name)}
        />
      </div>
    </div>
  );
};
