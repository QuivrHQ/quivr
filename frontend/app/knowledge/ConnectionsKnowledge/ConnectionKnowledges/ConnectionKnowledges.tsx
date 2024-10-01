import Image from "next/image";
import { useState } from "react";

import { SyncsByProvider } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import ConnectionAccount from "./ConnectionAccount/ConnectionAccount";
import styles from "./ConnectionKnowledges.module.scss";

interface ConnectionKnowledgeProps {
  providerGroup: SyncsByProvider;
}

const ConnectionKnowledges = ({
  providerGroup,
}: ConnectionKnowledgeProps): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const { providerIconUrls } = useSync();

  const transformConnectionLabel = (label: string): string => {
    switch (label) {
      case "Google":
        return "Google Drive";
      case "Azure":
        return "Sharepoint";
      case "DropBox":
        return "Dropbox";
      default:
        return label;
    }
  };

  return (
    <div className={styles.connection_knowledges_wrapper}>
      <div className={styles.provider_line_wrapper}>
        <Icon
          name={folded ? "chevronRight" : "chevronDown"}
          size="normal"
          color="dark-grey"
          handleHover={true}
          onClick={() => setFolded(!folded)}
        />
        <div className={styles.hoverable}>
          <Image
            src={providerIconUrls[providerGroup.provider]}
            alt={providerGroup.provider}
            width={18}
            height={18}
          />
          <span className={styles.provider_title}>
            {transformConnectionLabel(providerGroup.provider)}
          </span>
        </div>
      </div>
      <div className={`${styles.accounts} ${folded ? styles.folded : ""}`}>
        {providerGroup.syncs.map((sync, index) => (
          <ConnectionAccount
            key={sync.id}
            sync={sync}
            index={index}
            singleAccount={providerGroup.syncs.length === 1}
          />
        ))}
      </div>
    </div>
  );
};

export default ConnectionKnowledges;
