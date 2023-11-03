import { Fragment } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { EmailAuthContextType } from "@/app/(auth)/login/types";
import Button from "@/lib/components/ui/Button";
import { useAuthModes } from "@/lib/hooks/useAuthModes";

import { useMagicLinkLogin } from "./hooks/useMagicLinkLogin";

export const MagicLinkLogin = (): JSX.Element => {
  const { t } = useTranslation(["login", "translation"]);
  const { magicLink } = useAuthModes();
  const { handleMagicLinkLogin } = useMagicLinkLogin();
  const { watch } = useFormContext<EmailAuthContextType>();

  if (!magicLink) {
    return <Fragment />;
  }

  return (
    <Button
      isLoading={watch("isMagicLinkSubmitting")}
      className="bg-black text-white py-2 font-normal w-full"
      type="submit"
      onClick={() => void handleMagicLinkLogin()}
    >
      {t("magicLink", { ns: "login" })}
    </Button>
  );
};
