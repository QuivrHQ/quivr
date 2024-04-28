"use client";
import { UUID } from "crypto";
import { AnimatePresence, motion } from "framer-motion";

import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { Knowledge } from "@/lib/types/Knowledge";

import styles from "./KnowledgeTab.module.scss";
import KnowledgeTable from "./KnowledgeTable/KnowledgeTable";
import { useAddedKnowledge } from "./hooks/useAddedKnowledge";

type KnowledgeTabProps = {
  brainId: UUID;
  hasEditRights: boolean;
  allKnowledge: Knowledge[];
};
export const KnowledgeTab = ({
  brainId,
  allKnowledge,
}: KnowledgeTabProps): JSX.Element => {
  const { isPending } = useAddedKnowledge({
    brainId,
  });
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();

  if (isPending) {
    return <LoaderIcon size="big" color="accent" />;
  }

  if (allKnowledge.length === 0) {
    return (
      <div className={styles.knowledge_tab_wrapper}>
        <MessageInfoBox type="warning">
          This brain is empty! You can add knowledge by clicking on
          <QuivrButton
            label="Add knowledge"
            color="primary"
            iconName="add"
            onClick={() => setShouldDisplayFeedCard(true)}
          />
          .
        </MessageInfoBox>
      </div>
    );
  }

  return (
    <div className={styles.knowledge_tab_wrapper}>
      <motion.div layout className="w-full flex flex-col gap-5">
        <AnimatePresence mode="popLayout">
          <KnowledgeTable knowledgeList={allKnowledge} />
        </AnimatePresence>
      </motion.div>
    </div>
  );
};
