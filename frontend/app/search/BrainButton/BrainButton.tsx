"use client";

import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import styles from "./BrainButton.module.scss";

interface BrainButtonProps {
  brain: MinimalBrainForUser;
  newBrain: () => void;
}

const BrainButton = ({ brain, newBrain }: BrainButtonProps): JSX.Element => {
  const { setCurrentBrainId } = useBrainContext();
  const [hovered, setHovered] = useState(false);

  return (
    <div
      className={styles.brain_button_container}
      onClick={() => {
        setCurrentBrainId(brain.id);
        newBrain();
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className={styles.header}>
        <Icon
          name="brain"
          size="normal"
          color={hovered ? "primary" : "black"}
        />
        <span className={styles.name}>{brain.name}</span>
      </div>
      <span className={styles.description}>{brain.description}</span>
    </div>
  );
};

export default BrainButton;
