import Image from "next/image";
import { useEffect, useState } from "react";

import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { OpenedConnection, Provider, Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";

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
        <ConnectionLine
          label={connection.email}
          index={index}
          id={connection.id}
        />
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

const renderExistingConnections = ({
  existingConnections,
  folded,
  setFolded,
  fromAddKnowledge,
  handleGetSyncFiles,
  openedConnections,
}: {
  existingConnections: Sync[];
  folded: boolean;
  setFolded: (folded: boolean) => void;
  fromAddKnowledge: boolean;
  handleGetSyncFiles: (
    userSyncId: number,
    currentProvider: Provider
  ) => Promise<void>;
  openedConnections: OpenedConnection[];
}) => {
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
              submitted={openedConnections.some((openedConnection) => {
                return (
                  openedConnection.name === connection.name &&
                  openedConnection.submitted
                );
              })}
              onClick={() =>
                void handleGetSyncFiles(connection.id, connection.provider)
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
  const { providerIconUrls, getUserSyncs, getSyncFiles } = useSync();
  const {
    setCurrentSyncElements,
    setCurrentSyncId,
    setOpenedConnections,
    openedConnections,
    hasToReload,
    setHasToReload,
  } = useFromConnectionsContext();
  const [existingConnections, setExistingConnections] = useState<Sync[]>([]);
  const [folded, setFolded] = useState<boolean>(!fromAddKnowledge);

  const fetchUserSyncs = async () => {
    try {
      const res: Sync[] = await getUserSyncs();
      setExistingConnections(
        res.filter(
          (sync) =>
            Object.keys(sync.credentials).length !== 0 &&
            sync.provider === provider
        )
      );
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    void fetchUserSyncs();
  }, []);

  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === "visible" && !document.hidden) {
        void fetchUserSyncs();
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, []);

  useEffect(() => {
    if (hasToReload) {
      void fetchUserSyncs();
      setHasToReload(false);
    }
  }, [hasToReload]);

  const handleOpenedConnections = (userSyncId: number) => {
    const existingConnection = openedConnections.find(
      (connection) => connection.user_sync_id === userSyncId
    );

    if (!existingConnection) {
      const newConnection: OpenedConnection = {
        name:
          existingConnections.find((connection) => connection.id === userSyncId)
            ?.name ?? "",
        user_sync_id: userSyncId,
        id: undefined,
        provider: provider,
        submitted: false,
        selectedFiles: { files: [] },
        last_synced: "",
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
              src={providerIconUrls[provider]}
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
        {renderExistingConnections({
          existingConnections,
          folded,
          setFolded,
          fromAddKnowledge: !!fromAddKnowledge,
          handleGetSyncFiles,
          openedConnections,
        })}
      </div>
    </>
  );
};
