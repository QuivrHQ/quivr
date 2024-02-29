"use client";
import { UUID } from "crypto";
import { AnimatePresence, motion } from "framer-motion";

import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";

import styles from "./KnowledgeTab.module.scss";
import { KnowledgeTable } from "./KnowledgeTable/KnowledgeTable";
import { useAddedKnowledge } from "./hooks/useAddedKnowledge";

type KnowledgeTabProps = {
  brainId: UUID;
  hasEditRights: boolean;
};
export const KnowledgeTab = ({ brainId }: KnowledgeTabProps): JSX.Element => {
  const { isPending, allKnowledge } = useAddedKnowledge({
    brainId,
  });

  if (isPending) {
    return <LoaderIcon size="big" color="accent" />;
  }

  if (allKnowledge.length === 0) {
    return (
      <div className={styles.knowledge_tab_wrapper}>
        <MessageInfoBox
          type="warning"
          content="This brain is empty! You can add knowledge by clicking on the Add knowledge button."
        />
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
