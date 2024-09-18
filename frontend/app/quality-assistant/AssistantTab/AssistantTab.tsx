"use client";

import { useState } from "react";

import { FileInput } from "@/lib/components/ui/FileInput/FileInput";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import AssistantCard from "./AssistantCard/AssistantCard";
import styles from "./AssistantTab.module.scss";

import { AssistantCardType } from "../types/assistant";

const mockAssistants: AssistantCardType[] = [
  {
    name: "Compliance Check",
    description:
      "Allows analyzing the compliance of the information contained in documents against charter or regulatory requirements.",
    disabled: true,
    iconName: "assistant",
  },
  {
    name: "Consistency Check",
    description:
      "Ensures that the information in one document is replicated identically in another document.",
    iconName: "assistant",
  },
  {
    name: "Difference Detection",
    description:
      "Highlights differences between one document and another after modifications.",
    iconName: "assistant",
  },
];

const AssistantTab = (): JSX.Element => {
  const [assistantChoosed, setAssistantChoosed] = useState<string | undefined>(
    undefined
  );

  const handleFileChange = (file: File) => {
    console.log("Selected file:", file);
  };

  return (
    <div className={styles.assistant_tab_wrapper}>
      {!assistantChoosed ? (
        <div className={styles.content_section}>
          <span className={styles.title}>Choose an assistant</span>
          <div className={styles.assistant_choice_wrapper}>
            {mockAssistants.map((assistant, index) => (
              <div
                key={index}
                onClick={() => setAssistantChoosed(assistant.name)}
              >
                <AssistantCard assistantCard={assistant} />
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className={styles.form_wrapper}>
          <span className={styles.title}>{assistantChoosed}</span>
          <div className={styles.file_inputs_wrapper}>
            <FileInput label="Document 1" onFileChange={handleFileChange} />
            <FileInput label="Document 2" onFileChange={handleFileChange} />
          </div>
        </div>
      )}
      {assistantChoosed && (
        <div className={styles.buttons_wrapper}>
          <QuivrButton
            iconName="chevronLeft"
            label="Back"
            color="primary"
            onClick={() => setAssistantChoosed(undefined)}
          />
          <QuivrButton
            iconName="chevronRight"
            label="EXECUTE"
            color="primary"
            important={true}
          />
        </div>
      )}
    </div>
  );
};

export default AssistantTab;
