/* eslint-disable max-lines */
"use client";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import { StripePricingModal } from "@/lib/components/Stripe";
import Button from "@/lib/components/ui/Button";
import Card, { CardBody, CardHeader } from "@/lib/components/ui/Card";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { UserStatistics } from "./components";
import { ApiKeyConfig } from "./components/ApiKeyConfig";
import LanguageSelect from "./components/LanguageDropDown/LanguageSelect";
import ThemeSelect from "./components/ThemeSelect/ThemeSelect";

const UserPage = (): JSX.Element => {
  const { session } = useSupabase();
  const { userData } = useUserData();
  const is_premium = userData?.is_premium;

  if (!session) {
    redirectToLogin();
  }

  const { user } = session;
  const { t } = useTranslation([
    "translation",
    "user",
    "config",
    "monetization",
  ]);

  return (
    <main className="container lg:w-2/3 mx-auto py-10 px-5">
      <Card className="mb-5 shadow-sm hover:shadow-none">
        <CardHeader>
          <h2 className="font-bold text-xl">
            {t("accountSection", { ns: "config" })}
          </h2>
        </CardHeader>

        <CardBody className="flex flex-col items-stretch max-w-max gap-2">
          <div className="flex gap-5 items-center">
            <p>
              <strong>{t("email")}:</strong> <span>{user.email}</span>
            </p>
            <Link href={"/logout"}>
              <Button className="px-3 py-2" variant="secondary">
                {t("logoutButton")}
              </Button>
            </Link>
          </div>
          {is_premium === true ? null : (
            <StripePricingModal
              Trigger={<Button>{t("monetization:upgrade")}</Button>}
            />
          )}
        </CardBody>
      </Card>

      <Card className="mb-5 shadow-sm hover:shadow-none">
        <CardHeader>
          <h2 className="font-bold text-xl">
            {t("settings", { ns: "config" })}
          </h2>
        </CardHeader>

        <CardBody>
          <LanguageSelect />

          <ThemeSelect />
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
