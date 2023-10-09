import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

import { useGoogleLogin } from "./hooks/useGoogleLogin";

export const GoogleLoginButton = (): JSX.Element => {
  const { isPending, signInWithGoogle } = useGoogleLogin();
  const { t } = useTranslation(["login"]);

  return (
    <Button
      onClick={() => void signInWithGoogle()}
      isLoading={isPending}
      variant={"danger"}
      type="button"
      data-testid="google-login-button"
    >
      {t("googleLogin", { ns: "login" })}
    </Button>
  );
};
