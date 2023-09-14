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
        <div className="flex mt-1 flex-row w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2 pl-6">
          <div className="flex flex-1 items-center">
            <span className="text-1xl">{t("filesUploading")}</span>
          </div>
          <AiOutlineLoading3Quarters className="animate-spin text-3xl" />
        </div>
      )}

      <div
        className={
          shouldDisplayUploadCard ? "h-full flex flex-col flex-auto" : ""
        }
      >
        {shouldDisplayUploadCard && (
          <div className="flex flex-1 overflow-y-scroll shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
            <KnowledgeToFeed
              onClose={() => setShouldDisplayUploadCard(false)}
              contents={contents}
              addContent={addContent}
              removeContent={removeContent}
            />
          </div>
        )}
        <div className="flex mt-1 flex-col w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
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
