import { TFunction } from "i18next";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

export const isBrainDescriptionValid = (
  description: string,
  publish: (toast: ToastData) => void,
  t: TFunction<["translation", "brain", "config"]>
): boolean => {
  if (description.trim() === "") {
    publish({
      variant: "danger",
      text: t("descriptionRequired", { ns: "config" }),
    });

    return false;
  }

  return true;
};
