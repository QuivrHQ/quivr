import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { useKnowledgeContext } from "@/lib/context/KnowledgeProvider/hooks/useKnowledgeContext";

import { FeedItems } from "./components";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";
import { useKnowledgeToFeedInput } from "./hooks/useKnowledgeToFeedInput.ts";

type KnowledgeToFeedInputProps = {
  dispatchHasPendingRequests?: () => void;
  closeFeedInput?: () => void;
};

export const KnowledgeToFeedInput = ({
  dispatchHasPendingRequests,
  closeFeedInput,
}: KnowledgeToFeedInputProps): JSX.Element => {
  const { t } = useTranslation(["translation", "upload"]);
  const { feedBrain } = useKnowledgeToFeedInput({
    dispatchHasPendingRequests,
    closeFeedInput,
  });
  const { knowledgeToFeed } = useKnowledgeContext();

  return (
    <div className="px-20">
      <div className="flex flex-row gap-10 justify-between items-center mt-5">
        <FileUploader />
        <span className="whitespace-nowrap	">
          {`${t("and", { ns: "translation" })} / ${t("or", {
            ns: "translation",
          })}`}
        </span>
        <Crawler />
      </div>
      <FeedItems />
      <div className="flex justify-center mt-5">
        <Button
          disabled={knowledgeToFeed.length === 0}
          className="rounded-xl bg-purple-600 border-white"
          onClick={() => void feedBrain()}
        >
          {t("feed_form_submit_button", { ns: "upload" })}
        </Button>
      </div>
    </div>
  );
};
