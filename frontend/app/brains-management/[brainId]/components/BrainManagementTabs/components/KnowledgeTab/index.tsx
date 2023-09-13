"use client";
import { UUID } from "crypto";
import { AnimatePresence, motion } from "framer-motion";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Spinner from "@/lib/components/ui/Spinner";

import DocumentItem from "./DocumentItem";
import { useKnowledgeTab } from "./hooks/useFileManagementTab";

type KnowledgeTabProps = {
  brainId: UUID;
};
export const KnowledgeTab = ({ brainId }: KnowledgeTabProps): JSX.Element => {
  const { t } = useTranslation(["translation", "explore"]);
  const { documents, setDocuments, isPending } = useKnowledgeTab({
    brainId,
  });

  return (
    <main>
      <section className="w-full outline-none pt-10 flex flex-col gap-5 items-center justify-center p-6">
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-3xl font-bold text-center">
            {t("title", { ns: "explore" })}
          </h1>
          <h2 className="opacity-50">{t("subtitle", { ns: "explore" })}</h2>
        </div>
        {isPending ? (
          <Spinner />
        ) : (
          <motion.div layout className="w-full max-w-xl flex flex-col gap-5">
            {documents.length !== 0 ? (
              <AnimatePresence mode="popLayout">
                {documents.map((document) => (
                  <DocumentItem
                    key={document.name}
                    document={document}
                    setDocuments={setDocuments}
                  />
                ))}
              </AnimatePresence>
            ) : (
              <div className="flex flex-col items-center justify-center mt-10 gap-1">
                <p className="text-center">{t("empty", { ns: "explore" })}</p>
                <Link href="/upload">
                  <Button>{t("uploadButton")}</Button>
                </Link>
              </div>
            )}
          </motion.div>
        )}
      </section>
    </main>
  );
};
