"use client";
import { useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

import { FeedItemType } from "../../../../../../app/chat/[chatId]/components/ActionsBar/types";
import { isValidUrl } from "../helpers/isValidUrl";

type UseCrawlerProps = {
  addContent: (content: FeedItemType) => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useCrawler = ({ addContent }: UseCrawlerProps) => {
  const urlInputRef = useRef<HTMLInputElement | null>(null);
  const { session } = useSupabase();
  const { publish } = useToast();
  const { t } = useTranslation(["translation", "upload"]);
  const [urlToCrawl, setUrlToCrawl] = useState<string>("");
  const { track } = useEventTracking();

  if (session === null) {
    redirectToLogin();
  }

  const handleSubmit = () => {
    if (urlToCrawl === "") {
      return;
    }
    if (!isValidUrl(urlToCrawl)) {
      void track("URL_INVALID");
      publish({
        variant: "danger",
        text: t("invalidUrl"),
      });

      return;
    }
    void track("URL_CRAWLED");
    addContent({
      source: "crawl",
      url: urlToCrawl,
    });
    setUrlToCrawl("");
  };

  return {
    urlInputRef,
    urlToCrawl,
    setUrlToCrawl,
    handleSubmit,
  };
};
