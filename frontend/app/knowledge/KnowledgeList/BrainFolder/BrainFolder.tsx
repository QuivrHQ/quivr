"use client";
import Image from "next/image";
import { useRef, useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useAddedKnowledge } from "@/lib/hooks/useAddedKnowledge";
import { isUploadedKnowledge } from "@/lib/types/Knowledge";

import styles from "./BrainFolder.module.scss";

type BrainFolderProps = {
  brain: MinimalBrainForUser;
};

const BrainFolder = ({ brain }: BrainFolderProps): JSX.Element => {
  const { isDarkMode } = useUserSettingsContext();
  const { allKnowledge } = useAddedKnowledge({
    brainId: brain.id,
  });
  const [folded, setFolded] = useState<boolean>(true);
  const contentRef = useRef<HTMLDivElement>(null);

  const getContentHeight = (): string => {
    return folded ? "0" : `${contentRef.current?.scrollHeight}px`;
  };

  return (
    <div className={styles.brain_folder_wrapper}>
      <div
        className={styles.brain_folder_header}
        onClick={() => setFolded(!folded)}
      >
        <div className={styles.left}>
          <Icon
            size="small"
            name="chevronDown"
            color="black"
            classname={`${styles.icon_rotate} ${
              folded ? styles.icon_rotate_down : styles.icon_rotate_right
            }`}
          />
          <Image
            className={isDarkMode ? styles.dark_image : ""}
            src={
              brain.integration_logo_url
                ? brain.integration_logo_url
                : "/default_brain_image.png"
            }
            alt="logo_image"
            width={18}
            height={18}
          />
          <span>{brain.name}</span>
        </div>
      </div>
      <div
        ref={contentRef}
        className={`${styles.content_wrapper} ${
          folded ? styles.content_collapsed : styles.content_expanded
        }`}
        style={{ maxHeight: getContentHeight() }}
      >
        {allKnowledge.map((knowledge) => (
          <div key={knowledge.id} className={styles.knowledge}>
            {isUploadedKnowledge(knowledge) ? (
              <span className={styles.file_name}>{knowledge.fileName}</span>
            ) : (
              <a href={knowledge.url} target="_blank" rel="noopener noreferrer">
                {knowledge.url}
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BrainFolder;
