"use client";
import Link from "next/link";
import { Suspense } from "react";
import { useTranslation } from "react-i18next";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { Divider } from "@/lib/components/ui/Divider";

import { GoogleLoginButton } from "./components/GoogleLogin";
import { MagicLinkLogin } from "./components/MagicLinkLogin";
import { useLogin } from "./hooks/useLogin";

const Main = (): JSX.Element => {
  useLogin();

  const { t } = useTranslation(["translation", "login"]);

  return (
    <div className="w-screen h-screen bg-ivory" data-testid="sign-in-card">
      <main className="h-full flex flex-col items-center justify-center">
        <section className="w-full md:w-1/2 lg:w-1/3 flex flex-col gap-2">
          <Link href="/" className="flex justify-center">
            <QuivrLogo size={80} color="black" />
          </Link>
          <p className="text-center text-4xl font-medium">
            {t("talk_to", { ns: "login" })}{" "}
            <span className="text-primary">Quivr</span>
          </p>
          <div className="mt-5 flex flex-col">
            <MagicLinkLogin />
            <Divider text={t("or")} className="my-3 uppercase" />
            <GoogleLoginButton />
          </div>
          <p className="text-[10px] text-center">
            {t("restriction_message", { ns: "login" })}
          </p>
        </section>
      </main>
    </div>
  );
};

const Login = (): JSX.Element => {
  return (
    <Suspense fallback="Loading...">
      <Main />
    </Suspense>
  );
};

export default Login;
