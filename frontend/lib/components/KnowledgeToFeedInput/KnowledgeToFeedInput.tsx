import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import { FeedItems } from "./components";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";

export const KnowledgeToFeedInput = ({
  feedBrain,
}: {
  feedBrain: () => void;
}): JSX.Element => {
  const { t } = useTranslation(["translation", "upload"]);

  const { knowledgeToFeed } = useKnowledgeToFeedContext();

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
          className="rounded-xl bg-primary border-white"
          onClick={() => void feedBrain()}
          data-testid="submit-feed-button"
        >
          {t("feed_form_submit_button", { ns: "upload" })}
        </Button>
      </div>
    </div>
  );
};
