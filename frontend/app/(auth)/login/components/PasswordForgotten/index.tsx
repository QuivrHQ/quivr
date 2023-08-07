/* eslint-disable */
"use client";

import Button from "@/lib/components/ui/Button";
import { usePasswordForgotten } from "./hooks/usePasswordForgotten";
import { useTranslation } from "react-i18next";

type PasswordForgottenProps = {
  email: string;
  setEmail: (email: string) => void;
};

export const PasswordForgotten = ({
  email,
  setEmail,
}: PasswordForgottenProps) => {
  const { isPending, handleRecoverPassword } = usePasswordForgotten({
    email,
    setEmail,
  });
  const {t, i18n} = useTranslation(["login"]);

  return (
    <Button
      type="button"
      variant={"tertiary"}
      onClick={handleRecoverPassword}
      isLoading={isPending}
    >
      {t("forgottenPassword",{ ns: 'login' })}
    </Button>
  );
};
