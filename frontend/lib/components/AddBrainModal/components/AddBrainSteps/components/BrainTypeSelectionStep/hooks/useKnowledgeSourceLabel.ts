import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { useTranslation } from "react-i18next";

import { BrainType } from "@/lib/types/BrainConfig";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeSourceLabel = () => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const isCompositeBrainActivated = useFeatureIsOn("agent-brain");

  const knowledgeSourceOptions: {
    label: string;
    value: BrainType;
  }[] = [
    {
      label: t("knowledge_source_doc", { ns: "brain" }),
      value: "doc",
    },
    {
      label: t("knowledge_source_api", { ns: "brain" }),
      value: "api",
    },
  ];

  if (isCompositeBrainActivated) {
    knowledgeSourceOptions.push({
      label: t("knowledge_source_composite_brain", { ns: "brain" }),
      value: "composite",
    });
  }

  return {
    knowledgeSourceOptions,
  };
};
