"use client";
import Image from "next/image";
import Link from "next/link";
import { useTranslation } from "react-i18next";

export const Logo = (): JSX.Element => {
  const { t } = useTranslation(["vaccineTruth"]);

  return (
    <Link
      data-testid="app-logo"
      href={"/chat"}
      className="flex items-center gap-4"
    >
      <Image
        className="rounded-full"
        src={"/vt-logo.png"}
        alt="Vaccinetruth Logo"
        width={48}
        height={48}
      />
      <h1 className="font-bold">{t("vaccineTruthAi")}</h1>
    </Link>
  );
};
