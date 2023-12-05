import { TFunction } from "i18next";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

export const checkBrainName = (
  name: string,
  publish: (toast: ToastData) => void,
  t: TFunction<["translation", "brain", "config"]>
): void => {
  if (name.trim() === "") {
    publish({
      variant: "danger",
      text: t("nameRequired", { ns: "config" }),
    });

    return;
  }
};
