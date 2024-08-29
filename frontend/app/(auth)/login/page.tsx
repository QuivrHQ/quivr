"use client";
import Link from "next/link";
import { Suspense } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useAuthModes } from "@/lib/hooks/useAuthModes";

import { AzureLoginButton } from "./components/AzureLogin";
import { EmailLogin } from "./components/EmailLogin";
import { GoogleLoginButton } from "./components/GoogleLogin";
import { useLogin } from "./hooks/useLogin";
import styles from "./page.module.scss";
import { EmailAuthContextType } from "./types";

const projectName = process.env.NEXT_PUBLIC_PROJECT_NAME;

const Main = (): JSX.Element => {
  useLogin();
  const { googleSso, azureSso } = useAuthModes();
  const { isDarkMode } = useUserSettingsContext();

  const methods = useForm<EmailAuthContextType>({
    defaultValues: {
      email: "",
      password: "",
    },
  });
  const { t } = useTranslation(["translation", "login"]);

  return (
    <div className={styles.login_page_wrapper}>
      <section className={styles.section}>
        <Link href="/" className={styles.logo_link}>
          <QuivrLogo size={80} color={isDarkMode ? "white" : "black"} />
        </Link>
        <p className={styles.title}>
          {t("talk_to", { ns: "login" })}{" "}
          <span className={styles.primary_text}>
            {projectName ? projectName : "Quivr"}
          </span>
        </p>
        <div className={styles.form_container}>
          <FormProvider {...methods}>
            <EmailLogin />
          </FormProvider>

          {googleSso && <GoogleLoginButton />}
          {azureSso && <AzureLoginButton />}
        </div>
      </section>
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
