"use client";

import { useEffect, useState } from "react";

import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useUserData } from "@/lib/hooks/useUserData";
import { ButtonType } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import { Analytics } from "./BrainsTabs/components/Analytics/Analytics";
import { ManageBrains } from "./BrainsTabs/components/ManageBrains/ManageBrains";
import styles from "./page.module.scss";

const Studio = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Manage my brains");
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { setIsBrainCreationModalOpened } = useBrainCreationContext();
  const { allBrains } = useBrainContext();
  const { userData } = useUserData();

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

  const [buttons, setButtons] = useState<ButtonType[]>([
    {
      label: "Create brain",
      color: "primary",
      onClick: () => {
        setIsBrainCreationModalOpened(true);
      },
      iconName: "brain",
      tooltip:
        "You have reached the maximum number of brains allowed. Please upgrade your plan or delete some brains to create a new one.",
    },
    {
      label: "Add knowledge",
      color: "primary",
      onClick: () => {
        setShouldDisplayFeedCard(true);
      },
      iconName: "uploadFile",
    },
  ]);

  useEffect(() => {
    if (userData) {
      setButtons((prevButtons) => {
        return prevButtons.map((button) => {
          if (button.label === "Create brain") {
            return {
              ...button,
              disabled:
                userData.max_brains <=
                allBrains.filter((brain) => brain.brain_type === "doc").length,
            };
          }

          return button;
        });
      });
    }
  }, [userData?.max_brains, allBrains.length]);

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
