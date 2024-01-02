import { useTranslation } from "react-i18next";

import {
  Crawler,
  FeedItems,
  FileUploader,
} from "@/lib/components/KnowledgeToFeedInput/components";

export const KnowledgeToFeedInput = (): JSX.Element => {
  const { t } = useTranslation(["translation", "upload"]);

  return (
    <div>
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
    </div>
  );
};
