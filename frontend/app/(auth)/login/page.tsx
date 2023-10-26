"use client";
import Link from "next/link";
import { Suspense } from "react";
import { useTranslation } from "react-i18next";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { Divider } from "@/lib/components/ui/Divider";
import Field from "@/lib/components/ui/Field";

import { GoogleLoginButton } from "./components/GoogleLogin";
import { MagicLinkLogin } from "./components/MagicLinkLogin";
import { useLogin } from "./hooks/useLogin";

const Main = (): JSX.Element => {
  const { setEmail, email } = useLogin();
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
            <Field
              name="email"
              type="email"
              placeholder={t("email")}
              onChange={(e) => setEmail(e.target.value)}
              value={email}
              label="Email"
              inputClassName="py-1 mt-1 mb-3"
            />
            <MagicLinkLogin email={email} setEmail={setEmail} />
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
