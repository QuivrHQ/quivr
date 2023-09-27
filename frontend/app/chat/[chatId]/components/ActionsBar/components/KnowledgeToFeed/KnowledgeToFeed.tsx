import { useTranslation } from "react-i18next";
import { MdClose } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";

import { FeedItems } from "./components";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";
import { FeedItemType, FeedItemUploadType } from "../../types";

type FeedProps = {
  onClose: () => void;
  contents: FeedItemType[];
  addContent: (content: FeedItemType) => void;
  removeContent: (index: number) => void;
};
export const KnowledgeToFeed = ({
  onClose,
  contents,
  addContent,
  removeContent,
}: FeedProps): JSX.Element => {
  const { t } = useTranslation(["translation"]);

  const files: File[] = (
    contents.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

  return (
    <div className="flex-col w-full relative">
      <div className="absolute right-2 top-1">
        <Button variant={"tertiary"} onClick={onClose}>
          <span>
            <MdClose className="text-3xl" />
          </span>
        </Button>
      </div>
      <FileUploader addContent={addContent} files={files} />
      <Divider text={t("or")} className="m-5" />
      <Crawler addContent={addContent} />
      <FeedItems contents={contents} removeContent={removeContent} />
    </div>
  );
};
