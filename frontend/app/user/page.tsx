/* eslint-disable max-lines */
"use client";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Card, { CardBody, CardHeader } from "@/lib/components/ui/Card";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { UserStatistics } from "./components";
import { ApiKeyConfig } from "./components/ApiKeyConfig";
import { useLanguageHook } from "./components/LanguageDropDown/hooks/useLanguageHook";
/* eslint-disable-next-line sort-imports */
import { useTheme, type Theme } from "./components/ThemeSelect/hooks/useTheme";

const UserPage = (): JSX.Element => {
  const { session } = useSupabase();

  if (!session) {
    redirectToLogin();
  }

  const { theme, setTheme } = useTheme();
  const { allLanguages, currentLanguage, change } = useLanguageHook();
  const { user } = session;
  const { t } = useTranslation(["translation", "user", "config"]);

  return (
    <main className="py-10 px-5">
      <Card className="mb-5 shadow-sm hover:shadow-none">
        <CardHeader>
          <h2 className="font-bold text-xl">
            {t("accountSection", { ns: "config" })}
          </h2>
        </CardHeader>

        <CardBody>
          <p className="mb-3">
            <strong>{t("email")}:</strong> <span>{user.email}</span>
          </p>

          <div className="inline-block">
            <Link href={"/logout"}>
              <Button className="px-3 py-2" variant="secondary">
                {t("logoutButton")}
              </Button>
            </Link>
          </div>
        </CardBody>
      </Card>

      <Card className="mb-5 shadow-sm hover:shadow-none">
        <CardHeader>
          <h2 className="font-bold text-xl">
            {t("settings", { ns: "config" })}
          </h2>
        </CardHeader>

        <CardBody>
          <fieldset name="language" className="mb-2">
            <label
              className="block text-slate-700 dark:text-slate-300 mb-2"
              htmlFor="language"
            >
              {t("languageSelect")}
            </label>

            <select
              name="language"
              id="language"
              value={currentLanguage}
              onChange={(e) => change(e.target.value)}
              className="bg-slate-50 focus-visible:ring-0 border rounded dark:bg-black dark:text-white p-2 w-full md:w-1/2 lg:w-1/3"
            >
              {Object.keys(allLanguages).map((lang) => (
                <option value={lang} key={lang}>
                  {allLanguages[lang].label}
                </option>
              ))}
            </select>
          </fieldset>

          <fieldset name="theme" className="mb-2">
            <label
              className="block text-slate-700 dark:text-slate-300 mb-2"
              htmlFor="theme"
            >
              {t("themeSelect")}
            </label>
            <select
              name="theme"
              id="theme"
              value={theme}
              onChange={(e) => setTheme(e.target.value as Theme)}
              className="bg-slate-50 focus:outline-none focus-visible:ring-none border rounded dark:bg-black dark:text-white p-2 w-full md:w-1/2 lg:w-1/3"
            >
              <option value="dark">Dark</option>
              <option value="light">Light</option>
            </select>
          </fieldset>
        </CardBody>
      </Card>

      <Card className="mb-5 shadow-sm hover:shadow-none">
        <CardHeader>
          <h2 className="font-bold text-xl">
            {t("brainUsage", { ns: "user" })}
          </h2>
        </CardHeader>

        <CardBody>
          <UserStatistics />
        </CardBody>
      </Card>

      <Card className="mb-5 shadow-sm hover:shadow-none">
        <CardHeader>
          <h2 className="font-bold text-xl">{t("apiKey", { ns: "config" })}</h2>
        </CardHeader>

        <CardBody className="p-3 flex flex-col">
          <ApiKeyConfig />
        </CardBody>
      </Card>
    </main>
  );
};

export default UserPage;
