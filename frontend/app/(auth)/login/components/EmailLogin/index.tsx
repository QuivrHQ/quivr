"use client";

import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { Divider } from "@/lib/components/ui/Divider";
import { useAuthModes } from "@/lib/hooks/useAuthModes";

import { EmailInput } from "./components/EmailInput";
import { MagicLinkLogin } from "./components/MagicLinkLogin/MaginLinkLogin";
import { PasswordLogin } from "./components/PasswordLogin/PasswordLogin";
import { EmailAuthContextType } from "../../types";

export const EmailLogin = (): JSX.Element => {
  const { reset } = useFormContext();
  const { watch } = useFormContext<EmailAuthContextType>();

  const { t } = useTranslation(["login", "translation"]);
  const { password, magicLink } = useAuthModes();

  if (watch("isMagicLinkSubmitted")) {
    return (
      <div className="text-center flex flex-col gap-4">
        <p>
          {t("check_your_email.part1", { ns: "login" })}{" "}
          <span className="font-semibold">
            {t("check_your_email.magic_link", { ns: "login" })}
          </span>{" "}
          {t("check_your_email.part2", { ns: "login" })}
        </p>
        <div>
          <span>{t("cant_find", { ns: "login" })}</span>{" "}
          <span
            className="cursor-pointer underline"
            onClick={() => void reset()}
          >
            {t("try_again")}
          </span>
        </div>
      </div>
    );
  }

  return (
    <>
      <EmailInput />
      <PasswordLogin />
      {password && magicLink && (
        <Divider
          text={t("or", { ns: "translation" })}
          className="my-3 uppercase"
        />
      )}
      <MagicLinkLogin />
    </>
  );
};
