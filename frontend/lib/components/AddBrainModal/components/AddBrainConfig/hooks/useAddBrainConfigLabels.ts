import { useTranslation } from "react-i18next";

import { BrainStatus, BrainType } from "@/lib/types/brainConfig";
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAddBrainConfigLabels = () => {
  const { t } = useTranslation(["translation", "brain", "config"]);

  const brainStatusOptions: {
    label: string;
    value: BrainStatus;
  }[] = [
    {
      label: t("private_brain_label", { ns: "brain" }),
      value: "private",
    },
    {
      label: t("public_brain_label", { ns: "brain" }),
      value: "public",
    },
  ];

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

  return {
    brainStatusOptions,
    knowledgeSourceOptions,
  };
};
