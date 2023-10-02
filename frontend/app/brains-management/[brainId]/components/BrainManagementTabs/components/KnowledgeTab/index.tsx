"use client";
import { UUID } from "crypto";
import { AnimatePresence, motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import Spinner from "@/lib/components/ui/Spinner";
import { KnowledgeToFeedProvider } from "@/lib/context";

import { AddKnowledge } from "./AddKnowledge";
import { KnowledgeTable } from "./KnowledgeTable";
import { useKnowledge } from "./hooks/useKnowledge";

type KnowledgeTabProps = {
  brainId: UUID;
};
export const KnowledgeTab = ({ brainId }: KnowledgeTabProps): JSX.Element => {
  const { t } = useTranslation(["translation", "explore"]);
  const { isPending, allKnowledge } = useKnowledge({
    brainId,
  });

  return (
    <KnowledgeToFeedProvider>
      <main>
        <section className="w-full outline-none pt-10 flex flex-col gap-5 items-center justify-center p-6">
          <div className="flex flex-col items-center justify-center">
            <h1 className="text-3xl font-bold text-center">
              {t("title", { ns: "explore" })}
            </h1>
            <h2 className="opacity-50">{t("subtitle", { ns: "explore" })}</h2>
          </div>
          <AddKnowledge />
          {isPending ? (
            <Spinner />
          ) : (
            <motion.div layout className="w-full max-w-xl flex flex-col gap-5">
              {allKnowledge.length !== 0 ? (
                <AnimatePresence mode="popLayout">
                  <KnowledgeTable knowledgeList={allKnowledge} />
                </AnimatePresence>
              ) : (
                <div className="flex flex-col items-center justify-center mt-10 gap-1">
                  <p className="text-center">{t("empty", { ns: "explore" })}</p>
                  <p className="text-center">
                    {t("feed_brain_instructions", { ns: "explore" })}
                  </p>
                </div>
              )}
            </motion.div>
          )}
        </section>
      </main>
    </KnowledgeToFeedProvider>
  );
};
