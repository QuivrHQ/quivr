import { useSync } from "@/lib/api/sync/useSync";

import { ConnectionSection } from "./ConnectionSection/ConnectionSection";
import styles from "./Connections.module.scss";

export const Connections = (): JSX.Element => {
  const { syncGoogleDrive, syncSharepoint } = useSync();

  return (
    <>
      <div className={styles.connections_wrapper}>
        <ConnectionSection
          label="Google Drive"
          iconUrl="https://quivr-cms.s3.eu-west-3.amazonaws.com/gdrive_8316d080fd.png"
          callback={(name) => void syncGoogleDrive(name)}
        />
        <ConnectionSection
          label="Sharepoint"
          iconUrl="https://quivr-cms.s3.eu-west-3.amazonaws.com/sharepoint_8c41cfdb09.png"
          callback={(name) => void syncSharepoint(name)}
        />
      </div>
    </>
  );
};
