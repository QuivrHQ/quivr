import Image from "next/image";
import { useState } from "react";

import { SyncsByProvider } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { transformConnectionLabel } from "@/lib/helpers/providers";

import ConnectionAccount from "./ConnectionAccount/ConnectionAccount";
import styles from "./ConnectionKnowledges.module.scss";

import { useKnowledgeContext } from "../../../KnowledgeProvider/hooks/useKnowledgeContext";

interface ConnectionKnowledgeProps {
  providerGroup: SyncsByProvider;
}

const ConnectionKnowledges = ({
  providerGroup,
}: ConnectionKnowledgeProps): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const { providerIconUrls } = useSync();
  const { setQuivrRootSelected, setCurrentFolder, setProviderRootSelected } =
    useKnowledgeContext();

  const selectProvider = () => {
    setCurrentFolder(undefined);
    setQuivrRootSelected(false);
    setProviderRootSelected(providerGroup.provider);
  };

  return (
    <div className={styles.connection_knowledges_wrapper}>
      <div
        className={styles.provider_line_wrapper}
        onClick={() => selectProvider()}
      >
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
