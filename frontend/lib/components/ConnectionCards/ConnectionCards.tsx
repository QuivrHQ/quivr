import { useSync } from "@/lib/api/sync/useSync";

import styles from "./ConnectionCards.module.scss";
import { ConnectionSection } from "./ConnectionSection/ConnectionSection";

interface ConnectionCardsProps {
  fromAddKnowledge?: boolean;
}

export const ConnectionCards = ({
  fromAddKnowledge,
}: ConnectionCardsProps): JSX.Element => {
  const { syncGoogleDrive, syncSharepoint, syncDropbox } = useSync();

  return (
    <div
      className={`${styles.connection_cards} ${
        fromAddKnowledge ? styles.spaced : ""
      }`}
    >
      <ConnectionSection
        label="Dropbox"
        provider="DropBox"
        callback={(name: string) => syncDropbox(name)}
      />
      <ConnectionSection
        label="Google Drive"
        provider="Google"
        callback={(name: string) => syncGoogleDrive(name)}
      />
      {/* <ConnectionSection
        label="Notion (Beta)"
        provider="Notion"
        callback={(name: string) => syncNotion(name)}
        oneAccountLimitation={true}
      /> */}
      <ConnectionSection
        label="Sharepoint"
        provider="Azure"
        callback={(name: string) => syncSharepoint(name)}
      />
    </div>
  );
};
