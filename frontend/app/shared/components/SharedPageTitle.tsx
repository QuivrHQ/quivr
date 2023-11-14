"use client";

import { useTranslation } from "react-i18next";

export const SharedPageTitle = (): JSX.Element => {
  const { t } = useTranslation(["vaccineTruth"]);

  return (
    <div className="py-4 text-center border-b border-solid w-full text-xs sm:text-sm">
      {t("sharedPageTitle", { version: "1.0.1" })}
    </div>
  );
};
