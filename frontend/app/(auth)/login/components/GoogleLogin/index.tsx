import { useTranslation } from "react-i18next";
import { FcGoogle } from "react-icons/fc";

import Button from "@/lib/components/ui/Button";

import { useGoogleLogin } from "./hooks/useGoogleLogin";

export const GoogleLoginButton = (): JSX.Element => {
  const { isPending, signInWithGoogle } = useGoogleLogin();
  const { t } = useTranslation(["login"]);

  return (
    <Button
      onClick={() => void signInWithGoogle()}
      isLoading={isPending}
      type="button"
      data-testid="google-login-button"
      className="font-normal bg-white text-black py-2 hover:text-white"
    >
      <FcGoogle />
      {t("googleLogin", { ns: "login" })}
    </Button>
  );
};
