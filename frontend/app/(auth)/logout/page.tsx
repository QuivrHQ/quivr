/* eslint-disable */
"use client";
import Link from "next/link";

import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";
import PageHeading from "@/lib/components/ui/PageHeading";
import { useLogout } from "./hooks/useLogout";
import { useTranslation } from "react-i18next";
import { Suspense } from "react";

export default function Logout() {

  const {t, i18n} = useTranslation(["translation","logout"]);

  const { handleLogout, isPending } = useLogout();

  function Logout() {
    return (
      <main data-testid="logout-page">
        <section className="w-full min-h-[80vh] h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
          <PageHeading title={t("title",{ ns: "logout" })} subtitle={t("subtitle",{ ns: "logout" })} />
          <Card className="max-w-md w-full p-5 sm:p-10 text-center flex flex-col items-center gap-5">
            <h2 className="text-lg">{t("areYouSure",{ ns: "logout" })}</h2>
            <div className="flex gap-5 items-center justify-center">
              <Link href={"/"}>
                <Button variant={"primary"}>{t("cancel",{ ns: "logout" })}</Button>
              </Link>
              <Button
                isLoading={isPending}
                variant={"danger"}
                onClick={() => handleLogout()}
                data-testid="logout-button"
              >
                {t("logoutButton")}
              </Button>
            </div>
          </Card>
        </section>
      </main>
    );
  }

  return (
    <Suspense fallback={"Loading..."}>
      <Logout />
    </Suspense>
  )
  
}
