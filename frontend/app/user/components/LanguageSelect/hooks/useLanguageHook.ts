import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useEventTracking } from "@/services/analytics/june/useEventTracking";

export const languages = {
  en: {
    label: "English",
  },
  es: {
    label: "Español",
  },
  fr: {
    label: "Français",
  },
  ptbr: {
    label: "Português",
  },
  ru: {
    label: "Русский",
  },
  zh_cn: {
    label: "简体中文",
  },
};

export type Language = {
  [key: string]: {
    label: string;
  };
};

export const useLanguageHook = (): {
  change: (newLanguage: string) => void;
  allLanguages: Language;
  currentLanguage: string | undefined;
} => {
  const { i18n } = useTranslation();
  const [allLanguages, setAllLanguages] = useState<Language>({});
  const [currentLanguage, setCurrentLanguage] = useState<string | undefined>();
  const { track } = useEventTracking();

  useEffect(() => {
    setAllLanguages(languages);

    // get language from localStorage
    const savedLanguage = localStorage.getItem("selectedLanguage") ?? "en";

    setCurrentLanguage(savedLanguage);
    void i18n.changeLanguage(savedLanguage);
  }, [i18n]);

  const change = (newLanguage: string) => {
    void track("CHANGE_LANGUAGE");
    setCurrentLanguage(newLanguage);
    localStorage.setItem("selectedLanguage", newLanguage);
    void i18n.changeLanguage(newLanguage);
  };

  return {
    change,
    allLanguages,
    currentLanguage,
  };
};
