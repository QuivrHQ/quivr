import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

import { FeedItems } from "./components";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";
import { useKnowledgeToFeedInput } from "./hooks/useKnowledgeToFeedInput.ts";
import { FeedItemUploadType } from "../../../app/chat/[chatId]/components/ActionsBar/types";

type KnowledgeToFeedInputProps = {
  dispatchHasPendingRequests?: () => void;
  closeFeedInput?: () => void;
};

export const KnowledgeToFeedInput = ({
  dispatchHasPendingRequests,
  closeFeedInput,
}: KnowledgeToFeedInputProps): JSX.Element => {
  const { t } = useTranslation(["translation", "upload"]);
  const { addContent, contents, feedBrain, removeContent } =
    useKnowledgeToFeedInput({
      dispatchHasPendingRequests,
      closeFeedInput,
    });

  const files: File[] = (
    contents.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

  return (
    <>
      <div className="flex flex-row gap-10 justify-between px-20 items-center mt-5">
        <FileUploader addContent={addContent} files={files} />
        <span className="whitespace-nowrap	">
          {`${t("and", { ns: "translation" })} / ${t("or", {
            ns: "translation",
          })}`}
        </span>
        <Crawler addContent={addContent} />
        <FeedItems contents={contents} removeContent={removeContent} />
      </div>
      <div className="flex justify-center mt-5">
        <Button
          disabled={contents.length === 0}
          className="rounded-xl bg-purple-600 border-white"
          onClick={() => void feedBrain()}
        >
          {t("feed_form_submit_button", { ns: "upload" })}
        </Button>
      </div>
    </>
  );
};
