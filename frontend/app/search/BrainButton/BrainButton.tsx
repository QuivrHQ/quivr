"use client";

import { UUID } from "crypto";
import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./BrainButton.module.scss";

export interface BrainOrModel {
  name: string;
  description: string;
  id?: UUID;
}
interface BrainButtonProps {
  brainOrModel: BrainOrModel;
  newBrain: () => void;
}

const BrainButton = ({
  brainOrModel,
  newBrain,
}: BrainButtonProps): JSX.Element => {
  const { setCurrentBrainId } = useBrainContext();
  const [hovered, setHovered] = useState(false);

  return (
    <div
      className={styles.brain_button_container}
      onClick={() => {
        if (brainOrModel.id) {
          setCurrentBrainId(brainOrModel.id);
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
        <span className={styles.name}>{brainOrModel.name}</span>
      </div>
      <span className={styles.description}>{brainOrModel.description}</span>
    </div>
  );
};

export default BrainButton;
