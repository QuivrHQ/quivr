"use client";

import { UUID } from "crypto";
import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./BrainButton.module.scss";

interface BrainButtonProps {
  name: string;
  description: string;
  id?: UUID;
  newBrain: () => void;
}

const BrainButton = ({
  name,
  description,
  id,
  newBrain,
}: BrainButtonProps): JSX.Element => {
  const { setCurrentBrainId } = useBrainContext();
  const [hovered, setHovered] = useState(false);

  return (
    <div
      className={styles.brain_button_container}
      onClick={() => {
        if (id) {
          setCurrentBrainId(id);
        }
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
        <span className={styles.name}>{name}</span>
      </div>
      <span className={styles.description}>{description}</span>
    </div>
  );
};

export default BrainButton;
