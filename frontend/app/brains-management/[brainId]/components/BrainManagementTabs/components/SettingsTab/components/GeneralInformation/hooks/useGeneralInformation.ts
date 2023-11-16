import { useTranslation } from "react-i18next";

import { BrainStatus, BrainType } from "@/lib/types/brainConfig";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useGeneralInformation = () => {
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

  const brainTypeOptions: {
    label: string;
    value: BrainType;
  }[] = [
    {
      value: "doc",
      label: t("knowledge_source_doc", { ns: "brain" }),
    },
    {
      label: t("knowledge_source_api", { ns: "brain" }),
      value: "api",
    },
  ];

  return {
    brainStatusOptions,
    brainTypeOptions,
  };
};
