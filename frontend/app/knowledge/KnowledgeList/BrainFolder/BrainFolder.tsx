"use client";
import Image from "next/image";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./BrainFolder.module.scss";

type BrainFolderProps = {
  brain: MinimalBrainForUser;
};

const BrainFolder = ({ brain }: BrainFolderProps): JSX.Element => {
  const { isDarkMode } = useUserSettingsContext();

  return (
    <div className={styles.brain_folder_wrapper}>
      <div className={styles.left}>
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
      </div>
    </div>
  );
};

export default BrainFolder;
