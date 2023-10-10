"use client";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";
import Field from "@/lib/components/ui/Field";
import PageHeading from "@/lib/components/ui/PageHeading";

import { useSignUp } from "./hooks/useSignUp";

const SignUp = (): JSX.Element => {
  const { handleSignUp, isPending, email, password, setEmail, setPassword } =
    useSignUp();
  const { t } = useTranslation(["translation", "signUp"]);

  return (
    <main data-testid="sign-up-page">
      <section className="min-h-[80vh] w-full h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading
          title={t("title", { ns: "signUp" })}
          subtitle={t("subtitle", { ns: "signUp" })}
        />
        <Card className="max-w-md w-full p-5 sm:p-10 text-left">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void handleSignUp();
            }}
            className="flex flex-col gap-2"
            data-testid="sign-up-form"
          >
            <Field
              name="email"
              required
              type="email"
              placeholder={t("email")}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              data-testid="email-field"
            />
            <Field
              name="password"
              required
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={t("password")}
              data-testid="password-field"
            />
            <div className="flex flex-col items-center justify-center mt-2 gap-2">
              <Button data-testid="sign-up-button" isLoading={isPending}>
                {t("signUpButton", { ns: "signUp" })}
              </Button>
              <Link href="/login">{t("login", { ns: "signUp" })}</Link>
            </div>
          </form>
        </Card>
      </section>
    </main>
  );
};

export default SignUp;
