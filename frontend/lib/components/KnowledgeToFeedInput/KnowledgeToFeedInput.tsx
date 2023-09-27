import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";

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
      <FileUploader addContent={addContent} files={files} />
      <Divider text={t("or", { ns: "translation" })} className="m-5" />
      <Crawler addContent={addContent} />
      <FeedItems contents={contents} removeContent={removeContent} />
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
