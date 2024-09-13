"use client";

import { useState } from "react";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { Tab } from "@/lib/types/Tab";

import styles from "./page.module.scss";

const QualityAssistant = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Assistant");

  const qualityAssistantTab: Tab[] = [
    {
      label: "Assistant",
      isSelected: selectedTab === "Assistant",
      onClick: () => setSelectedTab("Assistant"),
      iconName: "edit",
    },
    {
      label: "Process",
      isSelected: selectedTab === "Process",
      onClick: () => setSelectedTab("Process"),
      iconName: "graph",
    },
  ];

  return (
    <div className={styles.page_wrapper}>
      <div className={styles.page_header}>
        <PageHeader
          iconName="assistant"
          label="Quality Assistant"
          buttons={[]}
        />
      </div>
      <div className={styles.content_wrapper}>
        <Tabs tabList={qualityAssistantTab} />
      </div>
    </div>
  );
};

export default QualityAssistant;
