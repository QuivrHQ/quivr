"use client";

import styles from "./AssistantCard.module.scss";

import { AssistantCardType } from "../../types/assistant";

interface AssistantCardProps {
  assistantCard: AssistantCardType;
}

const AssistantCard = ({ assistantCard }: AssistantCardProps): JSX.Element => {
  return (
    <div
      className={`${styles.assistant_tab_wrapper} ${
        assistantCard.disabled ? styles.disabled : ""
      }`}
    >
      <span className={styles.title}>{assistantCard.name}</span>
      <span className={styles.description}>{assistantCard.description}</span>
    </div>
  );
};

export default AssistantCard;
