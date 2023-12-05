import { useTranslation } from "react-i18next";

import { BrainStatus } from "@/lib/types/brainConfig";
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainStatusOptions = () => {
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

  return {
    brainStatusOptions,
  };
};
