"use client";

import { useState } from "react";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { Tab } from "@/lib/types/Tab";

import AssistantTab from "./AssistantTab/AssistantTab";
import ProcessTab from "./ProcessTab/ProcessTab";
import styles from "./page.module.scss";

const QualityAssistant = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Assistants");

  const qualityAssistantTab: Tab[] = [
    {
      label: "Assistants",
      isSelected: selectedTab === "Assistants",
      onClick: () => setSelectedTab("Assistants"),
      iconName: "assistant",
    },
    {
      label: "Process",
      isSelected: selectedTab === "Process",
      onClick: () => setSelectedTab("Process"),
      iconName: "waiting",
    },
  ];

  return (
    <div className={styles.page_wrapper}>
      <div className={styles.page_header}>
        <PageHeader iconName="assistant" label="Assistants" buttons={[]} />
      </div>
      <div className={styles.content_wrapper}>
        <Tabs tabList={qualityAssistantTab} />
        {selectedTab === "Assistants" && (
          <AssistantTab setSelectedTab={setSelectedTab} />
        )}
        {selectedTab === "Process" && <ProcessTab />}
      </div>
    </div>
  );
};

export default QualityAssistant;
