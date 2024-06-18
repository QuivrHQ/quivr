import { useEffect, useMemo, useState } from "react";

import { useSync } from "@/lib/api/sync/useSync";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { Tab } from "@/lib/types/Tab";

import styles from "./KnowledgeToFeed.module.scss";
import { FromConnections } from "./components/FromConnections/FromConnections";
import { useFromConnectionsContext } from "./components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { FromDocuments } from "./components/FromDocuments/FromDocuments";
import { FromWebsites } from "./components/FromWebsites/FromWebsites";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

export const KnowledgeToFeed = ({
  hideBrainSelector,
}: {
  hideBrainSelector?: boolean;
}): JSX.Element => {
  const { allBrains, setCurrentBrainId, currentBrainId, currentBrain } =
    useBrainContext();
  const [selectedTab, setSelectedTab] = useState("Connections");
  const { knowledgeToFeed } = useKnowledgeToFeedContext();
  const { openedConnections, setOpenedConnections, setCurrentSyncId } =
    useFromConnectionsContext();
  const { getActiveSyncsForBrain } = useSync();

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
      label: "Connections",
      isSelected: selectedTab === "Connections",
      onClick: () => setSelectedTab("Connections"),
      iconName: "sync",
      badge: openedConnections.filter((connection) => connection.submitted)
        .length,
    },
    {
      label: "Documents",
      isSelected: selectedTab === "Documents",
      onClick: () => setSelectedTab("Documents"),
      iconName: "file",
      badge: knowledgeToFeed.filter(
        (knowledge) => knowledge.source === "upload"
      ).length,
    },
    {
      label: "Websites' page",
      isSelected: selectedTab === "Websites",
      onClick: () => setSelectedTab("Websites"),
      iconName: "website",
      badge: knowledgeToFeed.filter((knowledge) => knowledge.source === "crawl")
        .length,
    },
  ];

  useEffect(() => {
    if (currentBrain) {
      void (async () => {
        try {
          const res = await getActiveSyncsForBrain(currentBrain.id);
          setCurrentSyncId(undefined);
          setOpenedConnections(
            res.map((sync) => ({
              user_sync_id: sync.syncs_user_id,
              id: sync.id,
              provider: sync.syncs_user.provider,
              submitted: true,
              selectedFiles: {
                files: [
                  ...(sync.settings.folders?.map((folder) => ({
                    id: folder,
                    name: undefined,
                    is_folder: true,
                  })) ?? []),
                  ...(sync.settings.files?.map((file) => ({
                    id: file,
                    name: undefined,
                    is_folder: false,
                  })) ?? []),
                ],
              },
              name: sync.name,
              last_synced: sync.last_synced,
            }))
          );
        } catch (error) {
          console.error(error);
        }
      })();
    }
  }, [currentBrainId]);

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
        {selectedTab === "Connections" && <FromConnections />}
        {selectedTab === "Documents" && <FromDocuments />}
        {selectedTab === "Websites" && <FromWebsites />}
      </div>
    </div>
  );
};
