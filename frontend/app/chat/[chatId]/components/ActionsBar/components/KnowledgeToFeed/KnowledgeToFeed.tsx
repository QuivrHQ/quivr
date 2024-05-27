import { useMemo, useState } from "react";

import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { Tab } from "@/lib/types/Tab";

import styles from "./KnowledgeToFeed.module.scss";
import { FromConnections } from "./components/FromConnections/FromConnections";
import { FromDocuments } from "./components/FromDocuments/FromDocuments";
import { FromWebsites } from "./components/FromWebsites/FromWebsites";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

export const KnowledgeToFeed = ({
  hideBrainSelector,
}: {
  hideBrainSelector?: boolean;
}): JSX.Element => {
  const { allBrains, setCurrentBrainId, currentBrain } = useBrainContext();
  const [selectedTab, setSelectedTab] = useState("Documents");

  const brainsWithUploadRights = formatMinimalBrainsToSelectComponentInput(
    useMemo(
      () =>
        allBrains.filter(
          (brain) =>
            requiredRolesForUpload.includes(brain.role) && !!brain.max_files
        ),
      [allBrains]
    )
  );

  const knowledgesTabs: Tab[] = [
    {
      label: "Documents",
      isSelected: selectedTab === "Documents",
      onClick: () => setSelectedTab("Documents"),
      iconName: "file",
    },
    {
      label: "Websites",
      isSelected: selectedTab === "Websites",
      onClick: () => setSelectedTab("Websites"),
      iconName: "website",
    },
    {
      label: "Connections",
      isSelected: selectedTab === "Connections",
      onClick: () => setSelectedTab("Connections"),
      iconName: "sync",
    },
  ];

  return (
    <div className={styles.knowledge_to_feed_wrapper}>
      {!hideBrainSelector && (
        <div className={styles.single_selector_wrapper}>
          <SingleSelector
            options={brainsWithUploadRights}
            onChange={setCurrentBrainId}
            selectedOption={
              currentBrain
                ? { label: currentBrain.name, value: currentBrain.id }
                : undefined
            }
            placeholder="Select a brain"
            iconName="brain"
          />
        </div>
      )}
      <Tabs tabList={knowledgesTabs} />
      <div className={styles.tabs_content_wrapper}>
        {selectedTab === "Documents" && <FromDocuments />}
        {selectedTab === "Websites" && <FromWebsites />}
        {selectedTab === "Connections" && <FromConnections />}
      </div>
    </div>
  );
};
