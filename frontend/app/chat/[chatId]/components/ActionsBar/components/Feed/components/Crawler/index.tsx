"use client";
import { useTranslation } from "react-i18next";
import { MdSend } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";

import { useCrawler } from "./hooks/useCrawler";
import { FeedItemType } from "../../types";

type CrawlerProps = {
  addContent: (content: FeedItemType) => void;
};

export const Crawler = ({ addContent }: CrawlerProps): JSX.Element => {
  const { urlInputRef, urlToCrawl, setUrlToCrawl } = useCrawler();
  const { t } = useTranslation(["translation", "upload"]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    addContent({
      source: "crawl",
      url: urlToCrawl,
    });
    setUrlToCrawl("");
  };

  return (
    <div className="w-full flex justify-center items-center">
      <div className="max-w-xl w-full">
        <form onSubmit={handleSubmit} className="w-full">
          <Field
            name="crawlurl"
            ref={urlInputRef}
            type="text"
            placeholder={t("webSite", { ns: "upload" })}
            className="w-full"
            value={urlToCrawl}
            onChange={(e) => setUrlToCrawl(e.target.value)}
            icon={
              <Button variant={"tertiary"}>
                <MdSend />
              </Button>
            }
          />
        </form>
      </div>
    </div>
  );
};
