"use client";

import styles from "./AssistantCard.module.scss";

import { AssistantCardType } from "../../types/assistant";

interface AssistantCardProps {
  assistantCard: AssistantCardType;
}

const AssistantCard = ({ assistantCard }: AssistantCardProps): JSX.Element => {
  return (
    <div className={styles.assistant_tab_wrapper}>{assistantCard.name}</div>
  );
};

export default AssistantCard;
