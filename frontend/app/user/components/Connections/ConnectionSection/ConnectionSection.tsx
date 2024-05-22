import Image from "next/image";
import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./ConnectionSection.module.scss";

interface ConnectionSectionProps {
  label: string;
  iconUrl: string;
}

export const ConnectionSection = ({
  label,
  iconUrl,
}: ConnectionSectionProps): JSX.Element => {
  const [folded, setFolded] = useState<boolean>(true);

  return (
    <div
      className={styles.connection_section_wrapper}
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
  );
};
