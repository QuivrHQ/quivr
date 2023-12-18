"use client";
import Image from "next/image";
import { useTranslation } from "react-i18next";

import { Disclaimer } from "@/lib/components/Disclaimer";
export const ChatGuide = (): JSX.Element => {
  const { t } = useTranslation(["vaccineTruth"]);

  return (
    <div className="flex flex-col justify-center items-center h-full">
      <Disclaimer />
      <div className="flex-1 flex flex-col justify-center items-center">
        <Image
          className="rounded-full w-16 h-16 mb-4"
          src={"/vt-logo.png"}
          alt="vaccinetruth.ai logo"
          height={64}
          width={64}
        ></Image>

        <div className="font-bold mb-2">{t("emptyChatTitle")}</div>
        <div className="text-xs text-slate-500">{t("emptyChatSubTitle")}</div>
      </div>
    </div>
  );
};
