"use client";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { Tab } from "@/lib/types/Tab";

import styles from "./page.module.scss";

const Studio = (): JSX.Element => {
  const studioTabs: Tab[] = [
    {
      label: "Manage my brains",
      isSelected: true,
      onClick: () => void 0,
    },
    {
      label: "Create brain",
      isSelected: false,
      onClick: () => void 0,
    },
    {
      label: "Analytics",
      isSelected: false,
      onClick: () => void 0,
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
