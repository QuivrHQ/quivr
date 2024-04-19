import { capitalCase } from "change-case";
import Image from "next/image";

import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./BrainCard.module.scss";

import { Tag } from "../Tag/Tag";
import Tooltip from "../Tooltip/Tooltip";

interface BrainCardProps {
  tooltip: string;
  selected?: boolean;
  imageUrl: string;
  brainName: string;
  tags: string[];
  callback: () => void;
  key: string;
  disabled?: boolean;
}

export const BrainCard = ({
  tooltip,
  selected,
  imageUrl,
  brainName,
  tags,
  callback,
  key,
  disabled,
}: BrainCardProps): JSX.Element => {
  const { isDarkMode } = useUserSettingsContext();

  return (
    <div
      key={key}
      className={`${styles.brain_card_container} ${
        disabled ? styles.disabled : ""
      }`}
      onClick={() => {
        callback();
      }}
    >
      <Tooltip tooltip={tooltip}>
        <div
          className={`${styles.brain_card_wrapper} ${
            selected ? styles.selected : ""
          }`}
        >
          <Image
            className={isDarkMode ? styles.dark_image : ""}
            src={imageUrl}
            alt={brainName}
            width={50}
            height={50}
          />
          <span className={styles.brain_title}>{brainName}</span>
          <div className={styles.tag_wrapper}>
            {tags[0] && <Tag color="primary" name={capitalCase(tags[0])} />}
          </div>
        </div>
      </Tooltip>
    </div>
  );
};
