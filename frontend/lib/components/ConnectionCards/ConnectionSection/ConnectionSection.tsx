import Image from "next/image";
import { useEffect, useState } from "react";

import { Provider, Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { iconList } from "@/lib/helpers/iconList";

import { ConnectionLine } from "./ConnectionLine/ConnectionLine";
import styles from "./ConnectionSection.module.scss";

import { ConnectionIcon } from "../../ui/ConnectionIcon/ConnectionIcon";
import { Icon } from "../../ui/Icon/Icon";
import Tooltip from "../../ui/Tooltip/Tooltip";

interface ConnectionSectionProps {
  label: string;
  provider: Provider;
  callback: (name: string) => Promise<{ authorization_url: string }>;
  oneAccountLimitation?: boolean;
}

export const ConnectionSection = ({
  label,
  provider,
  callback,
  oneAccountLimitation,
}: ConnectionSectionProps): JSX.Element => {
  const { providerIconUrls, getUserSyncs } = useSync();
  const [existingConnections, setExistingConnections] = useState<Sync[]>([]);
  const [folded, setFolded] = useState<boolean>(true);

  const fetchUserSyncs = async () => {
    try {
      const res: Sync[] = await getUserSyncs();
      setExistingConnections(
        res.filter(
          (sync) =>
            Object.keys(sync.credentials).length !== 0 &&
            sync.provider.toLowerCase() === provider.toLowerCase()
        )
      );
    } catch (error) {
      console.error(error);
    }
  };

  const getButtonIcon = (): keyof typeof iconList => {
    return existingConnections.filter(
      (connection) => connection.status !== "REMOVED"
    ).length > 0
      ? "add"
      : "sync";
  };

  const getButtonName = (): string => {
    return existingConnections.filter(
      (connection) => connection.status !== "REMOVED"
    ).length > 0
      ? "Add more"
      : "Connect";
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

  const connect = async () => {
    const res = await callback(
      Math.random().toString(36).substring(2, 15) +
        Math.random().toString(36).substring(2, 15)
    );
    if (res.authorization_url) {
      window.open(res.authorization_url, "_blank");
    }
  };

  const renderConnectionLines = (
    connections: Sync[],
    connectionFolded: boolean
  ) => {
    if (!connectionFolded) {
      return connections
        .filter((connection) => connection.status !== "REMOVED")
        .map((connection, index) => (
          <ConnectionLine
            key={index}
            label={connection.email}
            index={index}
            id={connection.id}
            warnUserOnDelete={provider === "Notion"}
          />
        ));
    } else {
      return (
        <div className={styles.folded}>
          {connections.map((connection, index) => (
            <ConnectionIcon
              key={index}
              letter={connection.email[0]}
              index={index}
            />
          ))}
        </div>
      );
    }
  };

  const renderExistingConnections = () => {
    const activeConnections = existingConnections.filter(
      (connection) => connection.status !== "REMOVED"
    );

    if (activeConnections.length === 0) {
      return null;
    }

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
        {renderConnectionLines(activeConnections, folded)}
      </div>
    );
  };

  return (
    <>
      <div className={styles.connection_section_wrapper}>
        <div className={styles.connection_section_header}>
          <div className={styles.left}>
            <Image
              src={providerIconUrls[provider.toLowerCase()]}
              alt={label}
              width={24}
              height={24}
            />
            <span className={styles.label}>{label}</span>
          </div>
          {!oneAccountLimitation || existingConnections.length === 0 ? (
            <QuivrButton
              iconName={getButtonIcon()}
              label={getButtonName()}
              color="primary"
              onClick={connect}
              small={true}
            />
          ) : existingConnections[0] &&
            existingConnections[0].status === "REMOVED" ? (
            <Tooltip tooltip={`We are deleting your connection.`}>
              <div className={styles.deleting_wrapper}>
                <Icon name="waiting" size="small" color="warning" />
                <span className={styles.deleting_mention}>Deleting</span>
              </div>
            </Tooltip>
          ) : null}
        </div>
        {renderExistingConnections()}
      </div>
    </>
  );
};
