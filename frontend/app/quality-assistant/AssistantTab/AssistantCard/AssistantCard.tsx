"use client";

import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./AssistantCard.module.scss";

import { Assistant } from "../../types/assistant";

interface AssistantCardProps {
  assistant: Assistant;
}

const AssistantCard = ({ assistant }: AssistantCardProps): JSX.Element => {
  return (
    <div
      className={`${styles.assistant_tab_wrapper} ${
        assistant.tags.includes("Disabled") ? styles.disabled : ""
      }`}
    >
      <div className={styles.header}>
        <Icon name="assistant" color="black" size="normal" />
        <span className={styles.title}>{assistant.name}</span>
      </div>
      <span className={styles.description}>{assistant.description}</span>
    </div>
  );
};

export default AssistantCard;
