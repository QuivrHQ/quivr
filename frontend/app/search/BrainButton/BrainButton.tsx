"use client";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import styles from "./BrainButton.module.scss";

interface BrainButtonProps {
  brain: MinimalBrainForUser;
}

const BrainButton = ({ brain }: BrainButtonProps): JSX.Element => {
  const { setCurrentBrainId } = useBrainContext();

  return (
    <div
      className={styles.brain_button_container}
      onClick={() => setCurrentBrainId(brain.id)}
    >
      <Icon name="brain" size="normal" color="black" />
      <span className={styles.name}>{brain.name}</span>
    </div>
  );
};

export default BrainButton;
