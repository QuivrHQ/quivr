"use client";

import { Icon } from "@/lib/components/ui/Icon/Icon";

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
      <div className={styles.header}>
        <Icon name={assistantCard.iconName} color="black" size="normal" />
        <span className={styles.title}>{assistantCard.name}</span>
      </div>
      <span className={styles.description}>{assistantCard.description}</span>
    </div>
  );
};

export default AssistantCard;
