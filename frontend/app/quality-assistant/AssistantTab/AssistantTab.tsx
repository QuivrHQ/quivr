"use client";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import AssistantCard from "./AssistantCard/AssistantCard";
import styles from "./AssistantTab.module.scss";

import { AssistantCardType } from "../types/assistant";

const mockAssistants: AssistantCardType[] = [
  {
    name: "Assistant 1",
    description: "Description 1",
  },
  {
    name: "Assistant 2",
    description: "Description 2",
  },
  {
    name: "Assistant 3",
    description: "Description 3",
  },
];

const AssistantTab = (): JSX.Element => {
  return (
    <div className={styles.assistant_tab_wrapper}>
      <div className={styles.content_section}>
        <span className={styles.title}>Choose an assistant</span>
        <div className={styles.assistant_choice_wrapper}>
          {mockAssistants.map((assistant, index) => (
            <div key={index}>
              <AssistantCard assistantCard={assistant} />
            </div>
          ))}
        </div>
      </div>
      <div className={styles.button_wrapper}>
        <QuivrButton
          iconName="chevronRight"
          label="Executer"
          color="primary"
          important={true}
        />
      </div>
    </div>
  );
};

export default AssistantTab;
