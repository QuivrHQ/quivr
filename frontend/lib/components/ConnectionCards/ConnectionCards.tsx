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
      className={`${styles.connection_cards} ${fromAddKnowledge ? styles.spaced : ""
        }`}
    >
      <ConnectionSection
        label="Google Drive"
        provider="Google"
        callback={(name) => syncGoogleDrive(name)}
        fromAddKnowledge={fromAddKnowledge}
      />
      <ConnectionSection
        label="Sharepoint"
        provider="Azure"
        callback={(name) => syncSharepoint(name)}
        fromAddKnowledge={fromAddKnowledge}
      />
      <ConnectionSection
        label="Dropbox"
        provider="DropBox"
        callback={(name) => syncDropbox(name)}
        fromAddKnowledge={fromAddKnowledge}
      />
    </div>
  );
};
