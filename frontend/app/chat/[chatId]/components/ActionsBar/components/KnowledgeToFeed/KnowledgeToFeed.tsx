import { useMemo, useState } from "react";

import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./KnowledgeToFeed.module.scss";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

export const KnowledgeToFeed = (): JSX.Element => {
  const { allBrains, setCurrentBrainId, currentBrain } = useBrainContext();
  const [selectedTab, setSelectedTab] = useState("From document");
  const brainsWithUploadRights = formatMinimalBrainsToSelectComponentInput(
    useMemo(
      () =>
        allBrains.filter((brain) =>
          requiredRolesForUpload.includes(brain.role)
        ),
      [allBrains]
    )
  );

  const knowledgesTabs: Tab[] = [
    {
      label: "From documents",
      isSelected: selectedTab === "From document",
      onClick: () => setSelectedTab("From document"),
      iconName: "edit",
    },
    {
      label: "From websites",
      isSelected: selectedTab === "From websites",
      onClick: () => setSelectedTab("From websites"),
      iconName: "graph",
    },
  ];

  return (
    <div className={styles.knowledge_to_feed_wrapper}>
      <div className={styles.single_selector_wrapper}>
        <SingleSelector
          options={brainsWithUploadRights}
          onChange={setCurrentBrainId}
          selectedOption={
            currentBrain
              ? { label: currentBrain.name, value: currentBrain.id }
              : undefined
          }
        />
      </div>
      <Tabs tabList={knowledgesTabs} />
    </div>
  );
};
