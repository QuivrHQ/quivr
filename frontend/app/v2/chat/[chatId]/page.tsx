"use client";

import { useTranslation } from "react-i18next";

import { ActionsBar, ShortCuts } from "./components";

const SelectedChatPage = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);

  return (
    <main className="flex flex-col w-full pt-10" data-testid="chat-page">
      <section className="flex flex-col flex-1 items-center w-full h-full min-h-[70vh]">
        <div className="flex flex-col items-center justify-center px-5">
          <h1 className="text-3xl font-bold text-center">
            {t("empty_brain_title_intro")}{" "}
            <span className="text-purple-500">{t("brains")}</span>
            {" !! "}
            <br />
            {t("empty_brain_title_prefix")}{" "}
            <span className="text-purple-500">{t("brain")}</span>{" "}
            {t("empty_brain_title_suffix")}
          </h1>
        </div>
        <div className="flex-1 flex flex-col mt-8 w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25 p-12 pt-10">
          <div className="flex flex-1 flex-col">
            <ShortCuts />
          </div>
          <ActionsBar />
        </div>
      </section>
    </main>
  );
};

export default SelectedChatPage;
