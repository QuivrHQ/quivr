import { useTranslation } from "react-i18next";

import { Divider } from "@/lib/components/ui/Divider";

import { FeedItems } from "./components";
import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";
import { FeedItemType, FeedItemUploadType } from "../../../../types";

type KnowledgeToFeedInputProps = {
  contents: FeedItemType[];
  addContent: (content: FeedItemType) => void;
  removeContent: (index: number) => void;
};

export const KnowledgeToFeedInput = ({
  contents,
  addContent,
  removeContent,
}: KnowledgeToFeedInputProps): JSX.Element => {
  const { t } = useTranslation(["translation"]);

  const files: File[] = (
    contents.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

  return (
    <>
      <FileUploader addContent={addContent} files={files} />
      <Divider text={t("or")} className="m-5" />
      <Crawler addContent={addContent} />
      <FeedItems contents={contents} removeContent={removeContent} />
    </>
  );
};
