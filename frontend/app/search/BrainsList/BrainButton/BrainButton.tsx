"use client";

import { UUID } from "crypto";
import Image from "next/image";
import { useState } from "react";

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
  snippet_emoji?: string;
  snippet_color?: string;
}
interface BrainButtonProps {
  brainOrModel: BrainOrModel;
  newBrain: () => void;
}

const BrainButton = ({
  brainOrModel,
  newBrain,
}: BrainButtonProps): JSX.Element => {
  const [optionsHovered, setOptionsHovered] = useState(false);
  const { setCurrentBrainId } = useBrainContext();

  return (
    <div
      className={`${styles.brain_button_container} ${
        optionsHovered ? styles.not_hovered : ""
      }`}
      onClick={() => {
        setCurrentBrainId(brainOrModel.id);
        newBrain();
      }}
    >
      <div className={styles.header}>
        <div className={styles.left}>
          {brainOrModel.image_url ? (
            <Image
              className={styles.brain_image}
              src={brainOrModel.image_url}
              alt="Brain or Model"
              width={24}
              height={24}
            />
          ) : (
            <div
              className={styles.brain_snippet}
              style={{ backgroundColor: brainOrModel.snippet_color }}
            >
              <span>{brainOrModel.snippet_emoji}</span>
            </div>
          )}
          <span className={styles.name}>
            {brainOrModel.display_name ?? brainOrModel.name}
          </span>
        </div>
        {brainOrModel.brain_type === "doc" && (
          <div
            onClick={(event) => {
              event.stopPropagation();
              window.location.href = `/studio/${brainOrModel.id}`;
            }}
            onMouseEnter={() => setOptionsHovered(true)}
            onMouseLeave={() => setOptionsHovered(false)}
          >
            <Icon
              name="options"
              size="small"
              color="black"
              handleHover={true}
            />
          </div>
        )}
      </div>
      <span className={styles.description}>{brainOrModel.description}</span>
    </div>
  );
};

export default BrainButton;
