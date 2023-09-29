"use client";
import { useTranslation } from "react-i18next";
import { MdSend } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";

import { useCrawler } from "./hooks/useCrawler";

export const Crawler = (): JSX.Element => {
  const { urlInputRef, urlToCrawl, handleSubmit, setUrlToCrawl } = useCrawler();
  const { t } = useTranslation(["translation", "upload"]);

  return (
    <div className="w-full flex justify-center items-center">
      <div className="max-w-xl w-full">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit();
          }}
          className="w-full"
        >
          <Field
            name="crawlurl"
            ref={urlInputRef}
            type="text"
            data-testid="urlToCrawlInput"
            placeholder={t("webSite", { ns: "upload" })}
            className="w-full"
            value={urlToCrawl}
            onChange={(e) => setUrlToCrawl(e.target.value)}
            icon={
              <Button data-testid="urlToCrawlInputSubmit" variant={"tertiary"}>
                <MdSend />
              </Button>
            }
          />
        </form>
      </div>
    </div>
  );
};
