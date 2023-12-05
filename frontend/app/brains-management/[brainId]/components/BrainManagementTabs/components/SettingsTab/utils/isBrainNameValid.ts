import { TFunction } from "i18next";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

export const isBrainNameValid = (
  name: string,
  publish: (toast: ToastData) => void,
  t: TFunction<["translation", "brain", "config"]>
): boolean => {
  if (name.trim() === "") {
    publish({
      variant: "danger",
      text: t("nameRequired", { ns: "config" }),
    });

    return false;
  }

  return true;
};
