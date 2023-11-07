import { Fragment } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import Field from "@/lib/components/ui/Field";
import { emailPattern } from "@/lib/config/patterns";
import { useAuthModes } from "@/lib/hooks/useAuthModes";

import { EmailAuthContextType } from "../../../types";

export const EmailInput = (): JSX.Element => {
  const { register } = useFormContext<EmailAuthContextType>();
  const { t } = useTranslation();
  const { password, magicLink } = useAuthModes();
  if (!password && !magicLink) {
    return <Fragment />;
  }

  return (
    <Field
      {...register("email", {
        required: true,
        pattern: emailPattern,
      })}
      placeholder={t("email", { ns: "login" })}
      label={t("email", { ns: "translation" })}
      inputClassName="py-1 mt-1 mb-3"
    />
  );
};
