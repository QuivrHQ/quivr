import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { iconList } from "@/lib/helpers/iconList";

import styles from "./BrainTypeSelection.module.scss";

interface BrainType {
  name: string;
  description: string;
  iconName: keyof typeof iconList;
}

export const BrainTypeSelection = ({
  brainType,
}: {
  brainType: BrainType;
}): JSX.Element => {
  const [isHovered, setIsHovered] = useState<boolean>(false);

  return (
    <div
      className={styles.brain_type_wrapper}
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
