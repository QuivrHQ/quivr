"use client";

import { useState } from "react";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import AssistantCard from "./AssistantCard/AssistantCard";
import styles from "./AssistantTab.module.scss";

import { AssistantCardType } from "../types/assistant";

const mockAssistants: AssistantCardType[] = [
  {
    name: "Use Case #1",
    description: "Description 1",
    disabled: true,
  },
  {
    name: "Use Case #2",
    description: "Description 2",
  },
  {
    name: "Use Case #3",
    description: "Description 3",
  },
];

const AssistantTab = (): JSX.Element => {
  const [assistantChoosed, setAssistantChoosed] = useState(false);

  return (
    <div className={styles.assistant_tab_wrapper}>
      <div className={styles.content_section}>
        <span className={styles.title}>Choose an assistant</span>
        <div className={styles.assistant_choice_wrapper}>
          {mockAssistants.map((assistant, index) => (
            <div key={index} onClick={() => setAssistantChoosed(true)}>
              <AssistantCard assistantCard={assistant} />
            </div>
          ))}
        </div>
      </div>
      {assistantChoosed && (
        <div className={styles.button_wrapper}>
          <QuivrButton
            iconName="chevronLeft"
            label="Back"
            color="primary"
            onClick={() => setAssistantChoosed(false)}
          />
        </div>
      )}
    </div>
  );
};

export default AssistantTab;
