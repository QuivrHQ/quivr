"use client";
import { UUID } from "crypto";

import { KMSElement } from "@/lib/api/sync/types";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";

import styles from "./KnowledgeTab.module.scss";
import KnowledgeTable from "./KnowledgeTable/KnowledgeTable";
import { useAddedKnowledge } from "./hooks/useAddedKnowledge";

type KnowledgeTabProps = {
  brainId: UUID;
  hasEditRights: boolean;
  allKnowledge: KMSElement[];
};
export const KnowledgeTab = ({
  brainId,
  allKnowledge,
  hasEditRights,
}: KnowledgeTabProps): JSX.Element => {
  const { isPending } = useAddedKnowledge({
    brainId,
  });

  if (!hasEditRights) {
    return (
      <div className={styles.knowledge_tab_container}>
        <div className={styles.knowledge_tab_wrapper}>
          <MessageInfoBox type="warning">
            You don&apos;t have permission to access the knowledge in this
            brain.
          </MessageInfoBox>
        </div>
      </div>
    );
  }

  if (isPending) {
    return <LoaderIcon size="big" color="accent" />;
  }

  return (
    <div className={styles.knowledge_tab_container}>
      <div className={styles.knowledge_tab_wrapper}>
        <KnowledgeTable
          knowledgeList={allKnowledge.filter(
            (knowledge) => !knowledge.is_folder
          )}
        />
      </div>
    </div>
  );
};
