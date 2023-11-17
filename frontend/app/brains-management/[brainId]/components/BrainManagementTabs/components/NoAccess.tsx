"use client";

import { useTranslation } from "react-i18next";

export const NoAccess = (): JSX.Element => {
  const { t } = useTranslation(["translation", "config", "brain"]);

  return (
    <div className="flex justify-center items-center mt-5">
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md">
        <strong className="font-bold mr-1">
          {t("ohno", { ns: "config" })}
        </strong>
        <span className="block sm:inline">
          {t("roleRequired", { ns: "config" })}
        </span>
        <p>{t("requireAccess", { ns: "config" })}</p>
      </div>
    </div>
  );
};
