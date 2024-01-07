"use client";

import { useTranslation } from "react-i18next";

import { useLanguageHook } from "./hooks/useLanguageHook";

const LanguageSelect = (): JSX.Element => {
  const { t } = useTranslation(["translation"]);
  const { allLanguages, currentLanguage, change } = useLanguageHook();

  return (
    <fieldset name="language" className="mb-2">
      <label
        className="block text-slate-700 dark:text-slate-300 mb-2"
        htmlFor="language"
      >
        {t("languageSelect")}
      </label>

      <select
        data-testid="language-select"
        name="language"
        id="language"
        value={currentLanguage}
        onChange={(e) => change(e.target.value)}
        className="bg-slate-50 focus-visible:ring-0 border rounded dark:bg-black dark:text-white p-2 w-full md:w-1/2 lg:w-1/3"
      >
        {Object.keys(allLanguages).map((lang) => (
          <option data-testid={`option-${lang}`} value={lang} key={lang}>
            {allLanguages[lang].label}
          </option>
        ))}
      </select>
    </fieldset>
  );
};

LanguageSelect.displayName = "LanguageSelect";

export default LanguageSelect;
