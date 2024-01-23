import { useTranslation } from "react-i18next";

import { BrainType } from "@/lib/types/BrainConfig";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useGeneralInformation = () => {
  const { t } = useTranslation(["translation", "brain", "config"]);

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
    brainTypeOptions,
  };
};
