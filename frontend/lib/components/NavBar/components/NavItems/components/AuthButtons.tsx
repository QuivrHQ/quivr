import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

export const AuthButtons = (): JSX.Element => {
  const pathname = usePathname();
  const { t } = useTranslation();

  if (pathname === "/signup") {
    return (
      <Link href={"/login"}>
        <Button variant={"secondary"}>{t("loginButton")}</Button>
      </Link>
    );
  }
  if (pathname === "/login") {
    return (
      <Link href={"/signup"}>
        <Button variant={"secondary"}>{t("signUpButton")}</Button>
      </Link>
    );
  }

  return (
    <Link href={"/login"}>
      <Button data-testid="login-button" variant={"secondary"}>
        {t("loginButton")}
      </Button>
    </Link>
  );
};
