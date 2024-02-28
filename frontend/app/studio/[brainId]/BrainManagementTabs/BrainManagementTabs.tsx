/* eslint-disable max-lines */

import { useState } from "react";

import Spinner from "@/lib/components/ui/Spinner";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { Tab } from "@/lib/types/Tab";

import { KnowledgeTab } from "./components/KnowledgeTab/KnowledgeTab";
import { PeopleTab } from "./components/PeopleTab/PeopleTab";
import { SettingsTab } from "./components/SettingsTab/SettingsTab";
import { useBrainFetcher } from "./hooks/useBrainFetcher";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";

export const BrainManagementTabs = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Settings");
  const { brainId, hasEditRights } = useBrainManagementTabs();

  const { brain, isLoading } = useBrainFetcher({
    brainId,
  });

  const brainManagementTabs: Tab[] = [
    {
      label: "Settings",
      isSelected: selectedTab === "Settings",
      onClick: () => setSelectedTab("Settings"),
      iconName: "settings",
    },
    {
      label: "People",
      isSelected: selectedTab === "People",
      onClick: () => setSelectedTab("People"),
      iconName: "user",
      disabled: !hasEditRights,
    },
    {
      label: "Knowledge",
      isSelected: selectedTab === "Knowledge",
      onClick: () => setSelectedTab("Knowledge"),
      iconName: "file",
      disabled: !hasEditRights || brain?.brain_type !== "doc",
    },
  ];

  if (!brainId) {
    return <div />;
  }

  if (isLoading) {
    return (
      <div className="flex w-full h-full justify-center items-center">
        <Spinner />
      </div>
    );
  }

  return (
    <>
      <Tabs tabList={brainManagementTabs} />
      {selectedTab === "Settings" && <SettingsTab brainId={brainId} />}
      {selectedTab === "People" && <PeopleTab brainId={brainId} />}
      {selectedTab === "Knowledge" && (
        <KnowledgeTab brainId={brainId} hasEditRights={hasEditRights} />
      )}
    </>
  );
};
