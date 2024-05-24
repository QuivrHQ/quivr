import { useSync } from "@/lib/api/sync/useSync";

import { ConnectionSection } from "./ConnectionSection/ConnectionSection";
import styles from "./Connections.module.scss";

export const Connections = (): JSX.Element => {
  const { syncGoogleDrive, syncSharepoint, iconUrls } = useSync();

  return (
    <div className={styles.connections_wrapper}>
      <span className={styles.title}>Link Apps You Want to Search Across</span>
      <div className={styles.connection_cards}>
        <ConnectionSection
          label="Google Drive"
          iconUrl={iconUrls.googleDrive}
          callback={(name) => syncGoogleDrive(name)}
        />
        <ConnectionSection
          label="Sharepoint"
          iconUrl={iconUrls.azure}
          callback={(name) => syncSharepoint(name)}
        />
      </div>
    </div>
  );
};
