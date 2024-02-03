"use client";

import { useTranslation } from "react-i18next";

import { useLanguageHook } from "./hooks/useLanguageHook";

const LanguageSelect = (): JSX.Element => {
  const { t } = useTranslation(["translation"]);
  const { allLanguages, currentLanguage, change } = useLanguageHook();

  return (
    <fieldset name="language">
      <label htmlFor="language">{t("languageSelect")}</label>

      <select
        data-testid="language-select"
        name="language"
        id="language"
        value={currentLanguage}
        onChange={(e) => change(e.target.value)}
      >
        {Object.keys(allLanguages).map((lang) => (
          <option data-testid={`option-${lang}`} value={lang} key={lang}>
            {allLanguages[lang].label} {allLanguages[lang].flag}
          </option>
        ))}
      </select>
    </fieldset>
  );
};

LanguageSelect.displayName = "LanguageSelect";

export default LanguageSelect;
