"use client";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { ButtonType } from "@/lib/types/QuivrButton";

import { BrainManagementTabs } from "./components";
import { useBrainManagement } from "./hooks/useBrainManagement";
import styles from "./page.module.scss";

const BrainsManagement = (): JSX.Element => {
  const { brain } = useBrainManagement();

  const buttons: ButtonType[] = [
    {
      label: "Delete brain",
      color: "dangerous",
      onClick: () => {
        console.info("hey");
      },
      iconName: "brain",
    },
  ];

  if (!brain) {
    return <></>;
  }

  return (
    <div className={styles.brain_management_wrapper}>
      <PageHeader iconName="brain" label={brain.name} buttons={buttons} />
      <div className={styles.content_wrapper}>
        <BrainManagementTabs />
      </div>
    </div>
  );
};

export default BrainsManagement;
