/* eslint-disable */
"use client";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import Spinner from "@/lib/components/ui/Spinner";
import { UserStats } from "@/lib/types/User";

import { USER_DATA_KEY } from "@/lib/api/user/config";
import { useUserApi } from "@/lib/api/user/useUserApi";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { useQuery } from "@tanstack/react-query";
import { UserStatistics } from "./components/UserStatistics";

const UserPage = (): JSX.Element => {
  const [userStats, setUserStats] = useState<UserStats>();
  const { session } = useSupabase();
  const { t } = useTranslation(["translation", "user"]);
  const { getUser } = useUserApi();

  const { data: userData } = useQuery({
    queryKey: [USER_DATA_KEY],
    queryFn: getUser,
  });

  useEffect(() => {
    if (userData !== undefined) {
      setUserStats(userData);
    }
  }, [userData]);
  if (session === null) {
    redirectToLogin();
  }

  return (
    <main className="w-full flex flex-col pt-10">
      <section className="flex flex-col justify-center items-center flex-1 gap-5 h-full">
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
