import { Fragment } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { EmailAuthContextType } from "@/app/(auth)/login/types";
import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { useAuthModes } from "@/lib/hooks/useAuthModes";

import { usePasswordLogin } from "./hooks/usePasswordLogin";

export const PasswordLogin = (): JSX.Element => {
  const { t } = useTranslation(["login"]);
  const { password } = useAuthModes();
  const { handlePasswordLogin } = usePasswordLogin();
  const { register, watch } = useFormContext<EmailAuthContextType>();

  if (!password) {
    return <Fragment />;
  }

  return (
    <div>
      <Field
        {...register("password", { required: true })}
        placeholder={t("password", { ns: "login" })}
        label={t("password", { ns: "login" })}
        inputClassName="py-1 mt-1 mb-3"
        type="password"
      />
      <Button
        isLoading={watch("isPasswordSubmitting")}
        variant="secondary"
        className="py-2 font-normal w-full mb-1"
        onClick={() => void handlePasswordLogin()}
      >
        {t("login")}
      </Button>
    </div>
  );
};
