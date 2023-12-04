import { UUID } from "crypto";
import { AnimatePresence, motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import Spinner from "@/lib/components/ui/Spinner";

import { useAddedKnowledge } from "./hooks/useAddedKnowledge";
import { KnowledgeTable } from "../KnowledgeTable/KnowledgeTable";

type AddedKnowledgeProps = {
  brainId: UUID;
};
export const AddedKnowledge = ({
  brainId,
}: AddedKnowledgeProps): JSX.Element => {
  const { isPending, allKnowledge } = useAddedKnowledge({
    brainId,
  });

  const { t } = useTranslation("explore");

  if (isPending) {
    return <Spinner />;
  }

  if (allKnowledge.length === 0) {
    return (
      <motion.div layout className="w-full max-w-xl flex flex-col gap-5">
        <div className="flex flex-col items-center justify-center mt-0 gap-1">
          <p className="text-center">{t("empty", { ns: "explore" })}</p>
          <p className="text-center">
            {t("feed_brain_instructions", { ns: "explore" })}
          </p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div layout className="w-full flex flex-col gap-5">
      <AnimatePresence mode="popLayout">
        <KnowledgeTable knowledgeList={allKnowledge} />
      </AnimatePresence>
    </motion.div>
  );
};
