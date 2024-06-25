import { useTranslation } from "react-i18next";
import { FcGoogle } from "react-icons/fc";

import Button from "@/lib/components/ui/Button";

import { useGoogleLogin } from "./hooks/useGoogleLogin";
import styles from "./index.module.scss";

export const GoogleLoginButton = (): JSX.Element => {
  const { isPending, signInWithGoogle } = useGoogleLogin();
  const { t } = useTranslation(["login"]);

  return (
    <Button
      onClick={() => void signInWithGoogle()}
      isLoading={isPending}
      type="button"
      className={styles.button}
    >
      <FcGoogle />
      {t("googleLogin", { ns: "login" })}
    </Button>
  );
};
