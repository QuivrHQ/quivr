"use client";
import { useTranslation } from "react-i18next";
import { MdSend } from "react-icons/md";

import Field from "@/lib/components/ui/Field";

import { useCrawler } from "./hooks/useCrawler";

export const Crawler = (): JSX.Element => {
  const { urlInputRef } = useCrawler();

  const { t } = useTranslation(["translation", "upload"]);

  return (
    <div className="w-full">
      <div className="flex justify-center gap-5 px-6">
        <div className="max-w-xl w-full">
          <div className="flex-col justify-center gap-5">
            <div className="h-32 flex gap-5 justify-center items-center px-5">
              <div className="text-center max-w-sm w-full flex flex-col gap-5 items-center">
                <Field
                  name="crawlurl"
                  ref={urlInputRef}
                  type="text"
                  placeholder={t("webSite", { ns: "upload" })}
                  className="w-full"
                  icon={<MdSend />}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
