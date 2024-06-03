import Image from "next/image";
import { useEffect, useState } from "react";

import { OpenedConnection } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/FromConnection-provider";
import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { Provider, Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import { ConnectionButton } from "./ConnectionButton/ConnectionButton";
import { ConnectionLine } from "./ConnectionLine/ConnectionLine";
import styles from "./ConnectionSection.module.scss";

import { ConnectionIcon } from "../../ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "../../ui/Icon/Icon";
import { TextButton } from "../../ui/TextButton/TextButton";

interface ConnectionSectionProps {
  label: string;
  provider: Provider;
  callback: (name: string) => Promise<{ authorization_url: string }>;
  fromAddKnowledge?: boolean;
}

const renderConnectionLines = (
  existingConnections: Sync[],
  folded: boolean
) => {
  if (!folded) {
    return existingConnections.map((connection, index) => (
      <div key={index}>
        <ConnectionLine label={connection.email} index={index} />
      </div>
    ));
  } else {
    return (
      <div className={styles.folded}>
        {existingConnections.map((connection, index) => (
          <div className={styles.negative_margin} key={index}>
            <ConnectionIcon letter={connection.email[0]} index={index} />
          </div>
        ))}
      </div>
    );
  }
};

const renderExistingConnections = (
  existingConnections: Sync[],
  folded: boolean,
  setFolded: (folded: boolean) => void,
  fromAddKnowledge: boolean,
  handleGetSyncFiles: (userSyncId: number, currentProvider: Provider) => void
) => {
  if (!!existingConnections.length && !fromAddKnowledge) {
    return (
      <div className={styles.existing_connections}>
        <div className={styles.existing_connections_header}>
          <span className={styles.label}>Connected accounts</span>
          <Icon
            name="settings"
            size="normal"
            color="black"
            handleHover={true}
            onClick={() => setFolded(!folded)}
          />
        </div>
        {renderConnectionLines(existingConnections, folded)}
      </div>
    );
  } else if (existingConnections.length > 0 && fromAddKnowledge) {
    return (
      <div className={styles.existing_connections}>
        {existingConnections.map((connection, index) => (
          <div key={index}>
            <ConnectionButton
              label={connection.email}
              index={index}
              onClick={() =>
                handleGetSyncFiles(connection.id, connection.provider)
              }
            />
          </div>
        ))}
      </div>
    );
  } else {
    return null;
  }
};

export const ConnectionSection = ({
  label,
  provider,
  fromAddKnowledge,
  callback,
}: ConnectionSectionProps): JSX.Element => {
  const { iconUrls, getUserSyncs, getSyncFiles } = useSync();
  const {
    setCurrentSyncElements,
    setCurrentSyncId,
    setOpenedConnections,
    openedConnections,
  } = useFromConnectionsContext();
  const [existingConnections, setExistingConnections] = useState<Sync[]>([]);
  const [folded, setFolded] = useState<boolean>(!fromAddKnowledge);

  useEffect(() => {
    void (async () => {
      try {
        const res: Sync[] = await getUserSyncs();
        setExistingConnections(
          res.filter(
            (sync) => !!sync.credentials.token && sync.provider === provider
          )
        );
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  const handleOpenedConnections = (userSyncId: number) => {
    const existingConnection = openedConnections.find(
      (connection) => connection.id === userSyncId
    );

    if (!existingConnection) {
      const newConnection: OpenedConnection = {
        id: userSyncId,
        provider: provider,
        submitted: false,
        allFiles: true,
        selectedFiles: [],
      };

      setOpenedConnections([...openedConnections, newConnection]);
    }
  };

  const handleGetSyncFiles = async (userSyncId: number) => {
    try {
      const res = await getSyncFiles(userSyncId);
      setCurrentSyncElements(res);
      setCurrentSyncId(userSyncId);
      handleOpenedConnections(userSyncId);
    } catch (error) {
      console.error("Failed to get sync files:", error);
    }
  };

  const connect = async () => {
    const res = await callback(
      Math.random().toString(36).substring(2, 15) +
        Math.random().toString(36).substring(2, 15)
    );
    if (res.authorization_url) {
      window.open(res.authorization_url, "_blank");
    }
  };

  return (
    <>
      <div className={styles.connection_section_wrapper}>
        <div className={styles.connection_section_header}>
          <div className={styles.left}>
            <Image
              src={iconUrls[provider]}
              alt={label}
              width={24}
              height={24}
            />
            <span className={styles.label}>{label}</span>
          </div>
          {!fromAddKnowledge ? (
            <QuivrButton
              iconName={existingConnections.length ? "add" : "sync"}
              label={existingConnections.length ? "Add more" : "Connect"}
              color="primary"
              onClick={() => connect()}
              small={true}
            />
          ) : (
            <TextButton
              iconName={existingConnections.length ? "add" : "sync"}
              label={existingConnections.length ? "Add more" : "Connect"}
              color="black"
              onClick={() => connect()}
              small={true}
            />
          )}
        </div>
        {renderExistingConnections(
          existingConnections,
          folded,
          setFolded,
          !!fromAddKnowledge,
          (userSyncId: number) => void handleGetSyncFiles(userSyncId)
        )}
      </div>
    </>
  );
};
