"use client";

import { UUID } from "crypto";
import Image from "next/image";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { BrainType } from "@/lib/types/BrainConfig";

import styles from "./BrainButton.module.scss";

export interface BrainOrModel {
  name: string;
  description: string;
  id: UUID;
  brain_type: BrainType;
  image_url?: string;
  price?: number;
  display_name?: string;
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

  return (
    <div
      className={styles.brain_button_container}
      onClick={() => {
        setCurrentBrainId(brainOrModel.id);
        newBrain();
      }}
    >
      <div className={styles.header}>
        {brainOrModel.image_url ? (
          <Image
            src={brainOrModel.image_url}
            alt="Brain or Model"
            width={16}
            height={16}
          />
        ) : (
          <Icon name="brain" size="normal" color="black" />
        )}
        <span className={styles.name}>
          {brainOrModel.display_name ?? brainOrModel.name}
        </span>
      </div>
      <span className={styles.description}>{brainOrModel.description}</span>
    </div>
  );
};

export default BrainButton;
