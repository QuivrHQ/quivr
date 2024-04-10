"use client";

import { useState } from "react";

import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { ButtonType } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import { Analytics } from "./BrainsTabs/components/Analytics/Analytics";
import { ManageBrains } from "./BrainsTabs/components/ManageBrains/ManageBrains";
import styles from "./page.module.scss";

const Studio = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Manage my brains");
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { setIsBrainCreationModalOpened } = useBrainCreationContext();

  const studioTabs: Tab[] = [
    {
      label: "Manage my brains",
      isSelected: selectedTab === "Manage my brains",
      onClick: () => setSelectedTab("Manage my brains"),
      iconName: "edit",
    },
    {
      label: "Analytics",
      isSelected: selectedTab === "Analytics",
      onClick: () => setSelectedTab("Analytics"),
      iconName: "graph",
    },
  ];

  const buttons: ButtonType[] = [
    {
      label: "Create brain",
      color: "primary",
      onClick: () => {
        setIsBrainCreationModalOpened(true);
      },
      iconName: "brain",
    },
    {
      label: "Add knowledge",
      color: "primary",
      onClick: () => {
        setShouldDisplayFeedCard(true);
      },
      iconName: "uploadFile",
    },
  ];

  return (
    <div className={styles.page_wrapper}>
      <div className={styles.page_header}>
        <PageHeader
          iconName="brainCircuit"
          label="Brain Studio"
          buttons={buttons}
        />
      </div>
      <div className={styles.content_wrapper}>
        <Tabs tabList={studioTabs} />
        {selectedTab === "Manage my brains" && <ManageBrains />}
        {selectedTab === "Analytics" && <Analytics />}
      </div>
      <UploadDocumentModal />
      <AddBrainModal />
    </div>
  );
};

export default Studio;
