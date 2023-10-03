"use client";

import { FormEvent } from "react";
import { useTranslation } from "react-i18next";

/* eslint-disable-next-line sort-imports */
import { useTheme, type Theme } from "./hooks/useTheme";

const ThemeSelect = (): JSX.Element => {
  const { theme, setTheme } = useTheme();
  const { t } = useTranslation(["translation"]);
  const handleChange = (e: FormEvent<HTMLSelectElement>) => {
    setTheme(e.currentTarget.value as Theme);
  };

  return (
    <fieldset name="theme" className="mb-2">
      <label
        className="block text-slate-700 dark:text-slate-300 mb-2"
        htmlFor="theme"
      >
        {t("themeSelect")}
      </label>

      <select
        data-testid="theme-select"
        name="theme"
        id="theme"
        value={theme}
        onChange={handleChange}
        className="bg-slate-50 focus:outline-none focus-visible:ring-none border rounded dark:bg-black dark:text-white p-2 w-full md:w-1/2 lg:w-1/3"
      >
        <option data-testid="theme-dark" value="dark">
          Dark
        </option>
        <option data-testid="theme-light" value="light">
          Light
        </option>
      </select>
    </fieldset>
  );
};

ThemeSelect.displayName = "ThemeSelect";

export default ThemeSelect;
