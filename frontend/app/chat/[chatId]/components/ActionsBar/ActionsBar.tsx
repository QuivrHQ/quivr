import { useTranslation } from "react-i18next";
import { AiOutlineLoading3Quarters } from "react-icons/ai";

import { ChatInput, KnowledgeToFeed } from "./components";
import { useActionBar } from "./hooks/useActionBar";
import { useKnowledgeUploader } from "./hooks/useKnowledgeUploader";

export const ActionsBar = (): JSX.Element => {
  const {
    shouldDisplayUploadCard,
    setShouldDisplayUploadCard,
    hasPendingRequests,
    setHasPendingRequests,
  } = useActionBar();

  const { addContent, contents, feedBrain, removeContent } =
    useKnowledgeUploader({
      setHasPendingRequests,
      setShouldDisplayUploadCard,
    });

  const { t } = useTranslation(["chat"]);

  return (
    <>
      {hasPendingRequests && (
        <div className="flex mt-1 flex-col md:flex-row w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2 md:p-6 pl-6">
          <div className="flex flex-1 items-center mb-2 md:mb-0">
            <span className="text-sm md:text-1xl">{t("feedingBrain")}</span>
          </div>
          <AiOutlineLoading3Quarters className="animate-spin text-2xl md:text-3xl self-center" />
        </div>
      )}

      <div className="">
        {shouldDisplayUploadCard && (
          <div className="flex flex-1 overflow-y-auto shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-4 md:p-6">
            <KnowledgeToFeed
              onClose={() => setShouldDisplayUploadCard(false)}
              contents={contents}
              addContent={addContent}
              removeContent={removeContent}
            />
          </div>
        )}
        <div className="flex mt-1 flex-col w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 md:mb-4 lg:mb-[-20px] p-2">
          <ChatInput
            shouldDisplayUploadCard={shouldDisplayUploadCard}
            setShouldDisplayUploadCard={setShouldDisplayUploadCard}
            feedBrain={() => void feedBrain()}
            hasContentToFeedBrain={contents.length > 0}
          />
        </div>
      </div>
    </>
  );
};
