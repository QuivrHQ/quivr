import Image from "next/image";
import { useEffect, useState } from "react";

import { Provider, Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import { ConnectionButton } from "./ConnectionButton/ConnectionButton";
import { ConnectionLine } from "./ConnectionLine/ConnectionLine";
import styles from "./ConnectionSection.module.scss";

import { ConnectionIcon } from "../../ui/ConnectionIcon/ConnectionIcon";
import Icon from "../../ui/Icon/Icon";
import { ConnectionModal } from "../ConnectionModal/ConnectionModal";

interface ConnectionSectionProps {
  label: string;
  provider: Provider;
  callback: (name: string) => Promise<{ authorization_url: string }>;
  fromAddKnowledge?: boolean;
}

export const ConnectionSection = ({
  label,
  provider,
  callback,
  fromAddKnowledge,
}: ConnectionSectionProps): JSX.Element => {
  const [connectionModalOpened, setConnectionModalOpened] =
    useState<boolean>(false);
  const { iconUrls, getUserSyncs } = useSync();
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
          <QuivrButton
            iconName={existingConnections.length ? "add" : "sync"}
            label={existingConnections.length ? "Add more" : "Connect"}
            color="primary"
            onClick={() => setConnectionModalOpened(true)}
            small={true}
          />
        </div>
        {!!existingConnections.length && !fromAddKnowledge && (
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
            {!folded ? (
              existingConnections.map((connection, index) => (
                <div key={index}>
                  <ConnectionLine label={connection.name} index={index} />
                </div>
              ))
            ) : (
              <div className={styles.folded}>
                {existingConnections.map((connection, index) => (
                  <div className={styles.negative_margin} key={index}>
                    <ConnectionIcon letter={connection.name[0]} index={index} />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
        {!!existingConnections.length &&
          fromAddKnowledge &&
          existingConnections.map((connection, index) => (
            <div key={index}>
              <ConnectionButton label={connection.name} index={index} />
            </div>
          ))}
      </div>
      <ConnectionModal
        modalOpened={connectionModalOpened}
        setModalOpened={setConnectionModalOpened}
        label={label}
        iconUrl={iconUrls[provider]}
        callback={(name) => callback(name)}
      />
    </>
  );
};
