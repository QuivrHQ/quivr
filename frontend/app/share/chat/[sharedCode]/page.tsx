"use client";

import Link from "next/link";
import { useTranslation } from "react-i18next";

import { DisplayChatMessageArea } from "@/lib/components/DisplayChatMessageArea";
import Spinner from "@/lib/components/ui/Spinner";

import { useSharedChatItems } from "../../components/hooks/useSharedChatItems";
const SharedChatPage = (): JSX.Element => {
  const { t } = useTranslation(["vaccineTruth"]);
  const { isLoading } = useSharedChatItems();

  return (
    <div
      className={`flex flex-col flex-1 items-center justify-stretch w-full h-fill-available overflow-hidden  dark:bg-black transition-colors ease-out duration-500`}
      data-testid="chat-page"
    >
      <div className="py-4 text-center border-b border-solid w-full text-xs sm:text-sm">
        Shared Chat • Vaccine truth knowledge base v1.0.1
      </div>
      <div
        className={`flex flex-col flex-1 w-full h-full dark:shadow-primary/25 overflow-hidden `}
      >
        <div className="flex flex-1 flex-col overflow-y-auto ">
          {isLoading ? (
            <div className="h-full flex justify-center items-center">
              <Spinner />
            </div>
          ) : (
            <DisplayChatMessageArea />
          )}
        </div>
      </div>
      <div className="fixed bottom-1 justify-center w-full bg-gradient-to-b from-transparent to-slate-300 flex">
        <Link
          className="text-xs sm:text-sm hover:text-lime-700 shadow-sm shadom-emerald-500 bg-emerald-500 rounded px-4 py-4 text-white hover:bg-emerald-300"
          href="/chat"
        >
          {t("talkToAI")}
        </Link>
      </div>
    </div>
  );
};

export default SharedChatPage;
