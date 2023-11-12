"use client";

import Link from "next/link";
import { useTranslation } from "react-i18next";

const TalkToVT = (): JSX.Element => {
  const { t } = useTranslation(["vaccineTruth"]);

  return (
    <div className="fixed bottom-1 justify-center w-full bg-gradient-to-b from-transparent to-slate-300 flex">
      <Link
        className="text-xs sm:text-sm hover:text-lime-700 shadow-sm shadom-emerald-500 bg-emerald-500 rounded px-4 py-4 text-white hover:bg-emerald-300"
        href="/chat"
      >
        {t("talkToAI")}
      </Link>
    </div>
  );
};

export default TalkToVT;
