"use client";
import { useTranslation } from "react-i18next";

import { DarkModeToggle } from "@/app/user/components/DarkModeToggle";
import { LanguageDropDown } from "@/app/user/components/LanguageDropDown";
import Spinner from "@/lib/components/ui/Spinner";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { UserStatistics } from "./components/UserStatistics";

const UserPage = (): JSX.Element => {
  const { session } = useSupabase();
  const { t } = useTranslation(["translation", "user"]);

  const { userData: userStats } = useUserData();

  if (session === null) {
    redirectToLogin();
  }

  return (
    <main className="w-full flex flex-col pt-10">
      <section className="flex flex-col justify-center items-center flex-1 gap-5 h-full">
        <div className="flex sm:flex-1 sm:justify-end flex-row items-center justify-center sm:flex-row gap-5 sm:gap-2">
          <LanguageDropDown />
          <DarkModeToggle />
        </div>
        <div className="p-5 max-w-3xl w-full min-h-full flex-1 mb-24">
          {userStats ? (
            <>
              <UserStatistics {...userStats} />
            </>
          ) : (
            <div className="flex items-center justify-center">
              <span>{t("fetching", { ns: "user" })}</span>
              <Spinner />
            </div>
          )}
        </div>
      </section>
    </main>
  );
};
export default UserPage;
