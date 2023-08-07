import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

export const AuthButtons = (): JSX.Element => {
  const pathname = usePathname();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const {t, i18n} = useTranslation();

  if (pathname === "/signup") {
    return (
      <Link href={"/login"}>
        <Button variant={"secondary"}>{t("loginButton")}</Button>
      </Link>
    );
  }
  else if (pathname === "/login") {
    return (
      <Link href={"/signup"}>
        <Button variant={"secondary"}>{t("signUpButton")}</Button>
      </Link>
    )
  } else {
    return (
      <Link href={"/login"}>
        <Button variant={"secondary"}>{t("loginButton")}</Button>
      </Link>
    );
  }

  
};
