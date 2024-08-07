"use client";

import { UUID } from "crypto";
import Image from "next/image";

import Icon from "@/lib/components/ui/Icon/Icon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./BrainButton.module.scss";

export interface BrainOrModel {
  name: string;
  description: string;
  image_url?: string;
  id?: UUID;
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
  const { setCurrentBrainId, setCurrentModel } = useBrainContext();

  return (
    <div
      className={styles.brain_button_container}
      onClick={() => {
        if (brainOrModel.id) {
          setCurrentBrainId(brainOrModel.id);
          setCurrentModel(null);
        } else {
          setCurrentModel({
            name: brainOrModel.name,
            display_name: brainOrModel.display_name ?? "",
            price: brainOrModel.price ?? 0,
            image_url: brainOrModel.image_url ?? "",
            description: brainOrModel.description,
          });
          setCurrentBrainId(null);
        }
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
