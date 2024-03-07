"use client";

import { useTranslation } from "react-i18next";

import { CountrySelector } from "@/lib/components/ui/CountrySelector/CountrySelector";

import { useLanguageHook } from "./hooks/useLanguageHook";

const LanguageSelect = (): JSX.Element => {
  const { t } = useTranslation(["translation"]);
  const { currentLanguage, change } = useLanguageHook();

  if (!currentLanguage) {
    return <></>;
  }

  return (
    <CountrySelector
      iconName="flag"
      label={t("languageSelect")}
      currentValue={currentLanguage}
      setCurrentValue={change}
    />
  );
};

LanguageSelect.displayName = "LanguageSelect";

export default LanguageSelect;
