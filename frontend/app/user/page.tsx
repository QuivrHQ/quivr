"use client";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Card, { CardBody, CardHeader } from "@/lib/components/ui/Card";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { StripePricingOrManageButton, UserStatistics } from "./components";
import { ApiKeyConfig } from "./components/ApiKeyConfig";
import LanguageSelect from "./components/LanguageSelect/LanguageSelect";
import { LogoutModal } from "./components/LogoutCard/LogoutModal";

const UserPage = (): JSX.Element => {
  const { session } = useSupabase();

  if (!session) {
    redirectToLogin();
  }

  const { user } = session;
  const { t } = useTranslation(["translation", "user", "config", "chat"]);

  return (
    <>
      <main className="container lg:w-2/3 mx-auto py-10 px-5">
        <Link href="/search">
          <Button className="mb-5" variant="primary">
            {t("chat:back_to_search")}
          </Button>
        </Link>
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

              <LogoutModal />
            </div>
            <StripePricingOrManageButton />
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
            <h2 className="font-bold text-xl">
              {t("apiKey", { ns: "config" })}
            </h2>
          </CardHeader>

          <CardBody className="p-3 flex flex-col">
            <ApiKeyConfig />
          </CardBody>
        </Card>
      </main>
    </>
  );
};

export default UserPage;
