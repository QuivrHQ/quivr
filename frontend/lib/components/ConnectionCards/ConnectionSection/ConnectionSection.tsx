import Image from "next/image";
import { useEffect, useState } from "react";

import { Provider, Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./ConnectionSection.module.scss";

import { ConnectionModal } from "../ConnectionModal/ConnectionModal";

interface ConnectionSectionProps {
  label: string;
  provider: Provider;
  callback: (name: string) => Promise<{ authorization_url: string }>;
}

export const ConnectionSection = ({
  label,
  provider,
  callback,
}: ConnectionSectionProps): JSX.Element => {
  const [connectionModalOpened, setConnectionModalOpened] =
    useState<boolean>(false);
  const { iconUrls, getUserSyncs } = useSync();
  const [existingConnections, setExistingConnections] = useState<Sync[]>([]);

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
          <Image src={iconUrls[provider]} alt={label} width={24} height={24} />
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
