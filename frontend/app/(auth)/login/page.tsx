"use client";
import Link from "next/link";
import { Suspense } from "react";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";
import { Divider } from "@/lib/components/ui/Divider";
import Field from "@/lib/components/ui/Field";
import PageHeading from "@/lib/components/ui/PageHeading";

import { GoogleLoginButton } from "./components/GoogleLogin";
import { MagicLinkLogin } from "./components/MagicLinkLogin";
import { PasswordForgotten } from "./components/PasswordForgotten";
import { useLogin } from "./hooks/useLogin";

const Main = (): JSX.Element => {
  const { handleLogin, setEmail, setPassword, email, isPending, password } =
    useLogin();
  const { t } = useTranslation(["translation", "login"]);

  return (
    <main>
      <section className="w-full min-h-[80vh] h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading
          title={t("title", { ns: "login" })}
          subtitle={t("subtitle", { ns: "login" })}
        />
        <Card className="max-w-md w-full p-5 sm:p-10 text-left">
          <form
            data-testid="sign-in-form"
            onSubmit={(e) => {
              e.preventDefault();
              void handleLogin();
            }}
            className="flex flex-col gap-2"
          >
            <Field
              name="email"
              required
              type="email"
              placeholder={t("email")}
              onChange={(e) => setEmail(e.target.value)}
              value={email}
            />
            <Field
              name="password"
              required
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={t("password")}
            />

            <div className="flex flex-col items-center justify-center mt-2 gap-2">
              <Button
                data-testid="submit-login"
                type="submit"
                isLoading={isPending}
              >
                {t("loginButton")}
              </Button>
              <PasswordForgotten setEmail={setEmail} email={email} />

              <Link href="/signup">{t("signup", { ns: "login" })}</Link>
            </div>

            <Divider text={t("or")} />
            <div className="flex flex-col items-center justify-center mt-2 gap-2">
              <GoogleLoginButton />
            </div>
            <Divider text={t("or")} />
            <MagicLinkLogin email={email} setEmail={setEmail} />
          </form>
        </Card>
      </section>
    </main>
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
