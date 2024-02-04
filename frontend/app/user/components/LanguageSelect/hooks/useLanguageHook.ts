import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useEventTracking } from "@/services/analytics/june/useEventTracking";

export type Language = {
  label: string;
  flag: string;
  shortName: string;
};

export const languages: Language[] = [
  {
    label: "English",
    flag: "🇬🇧",
    shortName: "en",
  },
  {
    label: "Español",
    flag: "🇪🇸",
    shortName: "es",
  },
  {
    label: "Français",
    flag: "🇫🇷",
    shortName: "fr",
  },
  {
    label: "Português",
    flag: "🇵🇹",
    shortName: "pt",
  },
  {
    label: "Русский",
    flag: "🇷🇺",
    shortName: "ru",
  },
  {
    label: "简体中文",
    flag: "🇨🇳",
    shortName: "zh",
  },
];

export const useLanguageHook = (): {
  change: (newLanguage: Language) => void;
  allLanguages: Language[];
  currentLanguage: Language | undefined;
} => {
  const { i18n } = useTranslation();
  const [allLanguages, setAllLanguages] = useState<Language[]>([]);
  const [currentLanguage, setCurrentLanguage] = useState<Language>();
  const { track } = useEventTracking();

  useEffect(() => {
    setAllLanguages(languages);
    const savedLanguage = localStorage.getItem("selectedLanguage") ?? "English";

    setCurrentLanguage(
      languages.find((language) => language.label === savedLanguage)
    );
    void i18n.changeLanguage(savedLanguage);
  }, [i18n]);

  const change = (newLanguage: Language) => {
    void track("CHANGE_LANGUAGE");
    setCurrentLanguage(newLanguage);
    localStorage.setItem("selectedLanguage", newLanguage.label);
    void i18n.changeLanguage(newLanguage.shortName);
  };

  return {
    change,
    allLanguages,
    currentLanguage,
  };
};
