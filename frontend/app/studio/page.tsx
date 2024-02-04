"use client";

import { useState } from "react";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { Tab } from "@/lib/types/Tab";

import styles from "./page.module.scss";

const Studio = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Manage my brains");

  const studioTabs: Tab[] = [
    {
      label: "Manage my brains",
      isSelected: selectedTab === "Manage my brains",
      onClick: () => setSelectedTab("Manage my brains"),
    },
    {
      label: "Create brain",
      isSelected: selectedTab === "Create brain",
      onClick: () => setSelectedTab("Create brain"),
    },
    {
      label: "Analytics",
      isSelected: selectedTab === "Analytics",
      onClick: () => setSelectedTab("Analytics"),
    },
  ];

  return (
    <div className={styles.page_wrapper}>
      <div className={styles.title_wrapper}>
        <Icon name="brainCircuit" size="big" color="primary" />
        <h1 className={styles.title}>Studio</h1>
      </div>
      <Tabs tabList={studioTabs} />
    </div>
  );
};

export default Studio;
