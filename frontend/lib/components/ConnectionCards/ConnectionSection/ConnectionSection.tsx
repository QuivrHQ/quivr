import Image from "next/image";
import { useState } from "react";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./ConnectionSection.module.scss";

import { ConnectionModal } from "../ConnectionModal/ConnectionModal";

interface ConnectionSectionProps {
  label: string;
  iconUrl: string;
  callback: (name: string) => Promise<{ authorization_url: string }>;
}

export const ConnectionSection = ({
  label,
  iconUrl,
  callback,
}: ConnectionSectionProps): JSX.Element => {
  const [connectionModalOpened, setConnectionModalOpened] =
    useState<boolean>(false);

  return (
    <>
      <div className={styles.connection_section_wrapper}>
        <div className={styles.connection_section_header}>
          <Image src={iconUrl} alt={label} width={24} height={24} />
          <span className={styles.label}>{label}</span>
        </div>
        <QuivrButton
          iconName="sync"
          label="Connect"
          color="primary"
          onClick={() => setConnectionModalOpened(true)}
          small={true}
        />
      </div>
      <ConnectionModal
        modalOpened={connectionModalOpened}
        setModalOpened={setConnectionModalOpened}
        label={label}
        iconUrl={iconUrl}
        callback={(name) => callback(name)}
      />
    </>
  );
};
