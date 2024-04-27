/* eslint-disable max-lines */

import { useEffect, useState } from "react";

import Spinner from "@/lib/components/ui/Spinner";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { Tab } from "@/lib/types/Tab";

import { KnowledgeTab } from "./components/KnowledgeTab/KnowledgeTab";
import { useAddedKnowledge } from "./components/KnowledgeTab/hooks/useAddedKnowledge";
import { PeopleTab } from "./components/PeopleTab/PeopleTab";
import { SettingsTab } from "./components/SettingsTab/SettingsTab";
import { useBrainFetcher } from "./hooks/useBrainFetcher";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";

export const BrainManagementTabs = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Settings");
  const { brainId, hasEditRights } = useBrainManagementTabs();
  const { allKnowledge } = useAddedKnowledge({ brainId: brainId ?? undefined });

  const { brain, isLoading } = useBrainFetcher({
    brainId,
  });

  const knowledgeTabDisabled = (): boolean => {
    return (
      !hasEditRights ||
      (brain?.integration_description?.max_files === 0 &&
        brain.brain_type !== "doc")
    );
  };

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
      label: `Knowledge${allKnowledge.length > 1 ? "s" : ""} (${
        allKnowledge.length
      })`,
      isSelected: selectedTab === "Knowledge",
      onClick: () => setSelectedTab("Knowledge"),
      iconName: "file",
      disabled: knowledgeTabDisabled(),
    },
  ];

  useEffect(() => {
    brainManagementTabs[2].disabled = knowledgeTabDisabled();
  }, [hasEditRights]);

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
        <KnowledgeTab
          brainId={brainId}
          hasEditRights={hasEditRights}
          allKnowledge={allKnowledge}
        />
      )}
    </>
  );
};
