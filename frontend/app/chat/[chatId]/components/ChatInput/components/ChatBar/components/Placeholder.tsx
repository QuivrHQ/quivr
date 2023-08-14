"use client";
import { useTranslation } from "react-i18next";

import { cn } from "@/lib/utils";

import { useConfiguration } from "./ConfigurationProvider";

export const Placeholder = () => {
  const { combobox } = useConfiguration();
  const { t } = useTranslation(["chat"]);

  return (
    <div
      className={cn(
        "pointer-events-none absolute inline-block select-none overflow-hidden overflow-ellipsis text-gray-500 dark:text-gray-400",
        combobox && "left-[14px] top-[18px]",
        !combobox && "left-3 top-4"
      )}
    >
      {t("actions_bar_placeholder")}
    </div>
  );
};
