import { useState } from "react";

import { BrainType } from "@/lib/components/AddBrainModal/types/types";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./BrainTypeSelection.module.scss";

export const BrainTypeSelection = ({
  brainType,
}: {
  brainType: BrainType;
}): JSX.Element => {
  const [isHovered, setIsHovered] = useState<boolean>(false);

  return (
    <div
      className={`
      ${styles.brain_type_wrapper} 
      ${brainType.disabled && styles.disabled}
      `}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={styles.first_line_wrapper}>
        <Icon
          name={brainType.iconName}
          size="normal"
          color={isHovered ? "primary" : "black"}
        />
        <span className={styles.name}>{brainType.name}</span>
      </div>
      <span className={styles.description}>{brainType.description}</span>
    </div>
  );
};
