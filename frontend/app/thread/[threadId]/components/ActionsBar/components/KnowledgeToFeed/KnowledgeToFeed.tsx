import { useMemo, useState } from "react";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { Tab } from "@/lib/types/Tab";

import styles from "./KnowledgeToFeed.module.scss";
import { FromDocuments } from "./components/FromDocuments/FromDocuments";
import { FromWebsites } from "./components/FromWebsites/FromWebsites";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

export const KnowledgeToFeed = ({
  hideBrainSelector,
}: {
  hideBrainSelector?: boolean;
}): JSX.Element => {
  const { allBrains, setCurrentBrainId, currentBrain } = useBrainContext();
  const [selectedTab, setSelectedTab] = useState("From documents");
  const { knowledgeToFeed, removeKnowledgeToFeed } =
    useKnowledgeToFeedContext();

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
      label: "From documents",
      isSelected: selectedTab === "From documents",
      onClick: () => setSelectedTab("From documents"),
      iconName: "file",
    },
    {
      label: "From websites",
      isSelected: selectedTab === "From websites",
      onClick: () => setSelectedTab("From websites"),
      iconName: "website",
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
        {selectedTab === "From documents" && <FromDocuments />}
        {selectedTab === "From websites" && <FromWebsites />}
      </div>
      <div>
        <div className={styles.uploaded_knowledges_title}>
          <span>Knowledges to upload</span>
          <span>{knowledgeToFeed.length}</span>
        </div>
        <div className={styles.uploaded_knowledges}>
          {knowledgeToFeed.map((knowledge, index) => (
            <div className={styles.uploaded_knowledge} key={index}>
              <div className={styles.left}>
                <Icon
                  name={knowledge.source === "crawl" ? "website" : "file"}
                  size="small"
                  color="black"
                />
                <span className={styles.label}>
                  {knowledge.source === "crawl"
                    ? knowledge.url
                    : knowledge.file.name}
                </span>
              </div>
              <Icon
                name="delete"
                size="normal"
                color="dangerous"
                handleHover={true}
                onClick={() => removeKnowledgeToFeed(index)}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
