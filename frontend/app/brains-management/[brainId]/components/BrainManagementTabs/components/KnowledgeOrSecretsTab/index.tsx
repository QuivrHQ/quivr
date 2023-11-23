"use client";
import { UUID } from "crypto";
import { useTranslation } from "react-i18next";

import { ApiBrainSecretsInputs } from "@/lib/components/ApiBrainSecretsInputs/ApiBrainSecretsInputs";
import { Divider } from "@/lib/components/ui/Divider";
import { KnowledgeToFeedProvider } from "@/lib/context";

import { AddKnowledge } from "./components/AddKnowledge/AddKnowledge";
import { AddedKnowledge } from "./components/AddedKnowledge/AddedKnowledge";
import { useBrainFetcher } from "../../hooks/useBrainFetcher";
import { NoAccess } from "../NoAccess";

type KnowledgeOrSecretsTabProps = {
  brainId: UUID;
  hasEditRights: boolean;
};
export const KnowledgeOrSecretsTab = ({
  brainId,
  hasEditRights,
}: KnowledgeOrSecretsTabProps): JSX.Element => {
  const { t } = useTranslation(["translation", "explore", "config"]);
  const { brain } = useBrainFetcher({
    brainId,
  });
  if (!hasEditRights) {
    return <NoAccess />;
  }

  if (brain?.brain_type === "api") {
    return <ApiBrainSecretsInputs brainId={brainId} />;
  }

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
          <Divider text={t("Upload")} />
          <AddKnowledge />
          <Divider
            text={t("knowledge", {
              ns: "config",
            })}
          />
          <AddedKnowledge brainId={brainId} />
        </section>
      </main>
    </KnowledgeToFeedProvider>
  );
};
