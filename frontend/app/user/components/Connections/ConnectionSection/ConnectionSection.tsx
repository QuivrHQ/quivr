import Image from "next/image";
import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionSection.module.scss";

import { ConnectionModal } from "../ConnectionModal/ConnectionModal";

interface ConnectionSectionProps {
  label: string;
  iconUrl: string;
}

export const ConnectionSection = ({
  label,
  iconUrl,
}: ConnectionSectionProps): JSX.Element => {
  const [folded, setFolded] = useState<boolean>(true);
  const [newConnectionHovered, setNewConnectionHovered] =
    useState<boolean>(false);
  const [connectionModalOpened, setConnectionModalOpened] =
    useState<boolean>(false);

  return (
    <>
      <div className={styles.connection_section_wrapper}>
        <div
          className={`${styles.connection_section_header} ${
            !folded ? styles.unfolded : ""
          }`}
          onClick={() => setFolded(!folded)}
        >
          <Icon
            name="chevronDown"
            size="normal"
            color="black"
            classname={`${styles.iconRotate} ${
              folded ? styles.iconRotateDown : styles.iconRotateRight
            }`}
          />
          <Image src={iconUrl} alt={label} width={24} height={24} />
          <span className={styles.label}>{label}</span>
        </div>
        {!folded && (
          <div className={styles.connection_section_content}>
            <div
              className={styles.new_connection}
              onMouseEnter={() => setNewConnectionHovered(true)}
              onMouseLeave={() => setNewConnectionHovered(false)}
            >
              <Icon
                name="add"
                color={newConnectionHovered ? "primary" : "black"}
                size="small"
              />
              <span>New Connection</span>
            </div>
          </div>
        )}
      </div>
      <ConnectionModal
        modalOpened={connectionModalOpened}
        setModalOpened={setConnectionModalOpened}
      />
    </>
  );
};
