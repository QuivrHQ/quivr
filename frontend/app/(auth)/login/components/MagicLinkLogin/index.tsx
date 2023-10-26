"use client";

import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { emailPattern } from "@/lib/config/patterns";

import { useMagicLinkLogin } from "./hooks/useMagicLinkLogin";

export const MagicLinkLogin = (): JSX.Element => {
  const {
    handleMagicLinkLogin,
    isSubmitting,
    register,
    isSubmitSuccessful,
    reset,
  } = useMagicLinkLogin();
  const { t } = useTranslation(["login", "translation"]);

  if (isSubmitSuccessful) {
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
    <form className="w-full" onSubmit={(e) => void handleMagicLinkLogin(e)}>
      <Field
        {...register("email", {
          required: true,
          pattern: emailPattern,
        })}
        placeholder={t("email", { ns: "login" })}
        label={t("email", { ns: "translation" })}
        inputClassName="py-1 mt-1 mb-3"
      />
      <Button
        isLoading={isSubmitting}
        className="bg-black text-white py-2 font-normal w-full"
      >
        {t("magicLink", { ns: "login" })}
      </Button>
    </form>
  );
};
