"use client";

import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

import { useMagicLinkLogin } from "./hooks/useMagicLinkLogin";

type MaginLinkLoginProps = {
  email: string;
  setEmail: (email: string) => void;
};

export const MagicLinkLogin = ({
  email,
  setEmail,
}: MaginLinkLoginProps): JSX.Element => {
  const { handleMagicLinkLogin, isPending } = useMagicLinkLogin({
    email,
    setEmail,
  });
  const { t } = useTranslation(["login"]);

  return (
    <Button
      type="button"
      variant={"tertiary"}
      onClick={() => void handleMagicLinkLogin()}
      isLoading={isPending}
    >
      {t("magicLink", { ns: "login" })}
    </Button>
  );
};
