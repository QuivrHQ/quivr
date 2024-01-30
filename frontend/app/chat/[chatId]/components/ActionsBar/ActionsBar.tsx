import { useTranslation } from "react-i18next";
import { AiOutlineLoading3Quarters } from "react-icons/ai";

import { ChatInput } from "./components";
import { useActionBar } from "./hooks/useActionBar";

export const ActionsBar = (): JSX.Element => {
  const { hasPendingRequests } = useActionBar();

  const { t } = useTranslation(["chat"]);

  return (
    <>
      {hasPendingRequests && (
        <div className="flex mt-1 flex-col md:flex-row w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2 md:p-6 pl-6 mb-3">
          <div className="flex flex-1 items-center mb-2 md:mb-0">
            <span className="text-sm md:text-1xl">{t("feedingBrain")}</span>
          </div>
          <AiOutlineLoading3Quarters className="animate-spin text-2xl md:text-3xl self-center" />
        </div>
      )}

      <div>
        <ChatInput />
      </div>
    </>
  );
};
