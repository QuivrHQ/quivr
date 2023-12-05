import { useTranslation } from "react-i18next";

import { BrainType } from "@/lib/types/brainConfig";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeSourceLabel = () => {
  const { t } = useTranslation(["translation", "brain", "config"]);

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
    {
      label: t("knowledge_source_chatflow", { ns: "brain" }),
      value: "chatflow",
    },
  ];

  return {
    knowledgeSourceOptions,
  };
};
