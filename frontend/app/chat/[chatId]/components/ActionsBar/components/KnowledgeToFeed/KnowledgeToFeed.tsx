import { useTranslation } from "react-i18next";
import { MdClose } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";

import { FeedItems } from "./components";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";
import { useKnowledgeToFeed } from "./hooks/useKnowledgeToFeed";

type FeedProps = {
  onClose: () => void;
};
export const KnowledgeToFeed = ({ onClose }: FeedProps): JSX.Element => {
  const { t } = useTranslation(["translation"]);
  const { addContent, contents, removeContent } = useKnowledgeToFeed();

  return (
    <div className="flex flex-col w-full table relative pb-5">
      <div className="absolute right-2 top-1">
        <Button variant={"tertiary"} onClick={onClose}>
          <span>
            <MdClose className="text-3xl" />
          </span>
        </Button>
      </div>
      <FileUploader />
      <Divider text={t("or")} className="m-5" />
      <Crawler addContent={addContent} />
      <FeedItems contents={contents} removeContent={removeContent} />
    </div>
  );
};
