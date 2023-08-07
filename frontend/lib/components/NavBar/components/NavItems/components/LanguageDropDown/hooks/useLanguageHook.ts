/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

export type Language = {
  id: string;
  name: string;
};

export const useLanguageHook = () => {
  const { i18n } = useTranslation();
  const [allLanguages, setAllLanguages] = useState<Language[]>([]);
  const [currentLanguage, setCurrentLanguage] = useState<Language | null>(null);

  useEffect(() => {
    const languages = [
      { 
        id: "en",
        name: 'English'
      },
      {
        id: "es",
        name: 'Español'
      }
    ];
    setAllLanguages(languages);
    setCurrentLanguage(languages[0]);
  }, []);

  const change = (newLanguage: Language) => {
    setCurrentLanguage(newLanguage);
    void i18n.changeLanguage(newLanguage.id);
  };

  return {
    change,
    allLanguages,
    currentLanguage
  };
};

