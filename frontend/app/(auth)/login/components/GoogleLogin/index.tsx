/* eslint-disable */
import Button from "@/lib/components/ui/Button";

import { useGoogleLogin } from "./hooks/useGoogleLogin";
import { useTranslation } from "react-i18next";

export const GoogleLoginButton = () => {
  const { isPending, signInWithGoogle } = useGoogleLogin();
  const {t, i18n} = useTranslation(["login"]);

  return (
    <Button
      onClick={signInWithGoogle}
      isLoading={isPending}
      variant={"danger"}
      type="button"
      data-testid="google-login-button"
    >
      {t("googleLogin",{ ns: 'login' })}
    </Button>
  );
};
