import { UUID } from "crypto";
import { useCallback, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { useCrawlApi } from "@/lib/api/crawl/useCrawlApi";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import { isValidUrl } from "../helpers/isValidUrl";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useCrawler = () => {
  const [isCrawling, setCrawling] = useState(false);
  const urlInputRef = useRef<HTMLInputElement | null>(null);
  const { session } = useSupabase();
  const { publish } = useToast();
  const { track } = useEventTracking();

  const { crawlWebsiteUrl } = useCrawlApi();
  if (session === null) {
    redirectToLogin();
  }

  const { t } = useTranslation(["translation", "upload"]);

  const crawlWebsite = useCallback(
    async (brainId: UUID | undefined) => {
      // Validate URL
      const url = urlInputRef.current ? urlInputRef.current.value : null;

      if (url === null || !isValidUrl(url)) {
        void track("URL_INVALID");

        publish({
          variant: "danger",
          text: t("invalidUrl", { ns: "upload" }),
        });

        return;
      }

      // Configure parameters
      const config = {
        url: url,
        js: false,
        depth: 1,
        max_pages: 100,
        max_time: 60,
      };

      setCrawling(true);

      void track("URL_CRAWLED");

      try {
        console.log("Crawling website...", brainId);
        if (brainId !== undefined) {
          const response = await crawlWebsiteUrl({
            brainId,
            config,
          });

          publish({
            variant: response.data.type,
            text: response.data.message,
          });
        }
      } catch (error: unknown) {
        publish({
          variant: "danger",
          text: t("crawlFailed", {
            message: JSON.stringify(error),
            ns: "upload",
          }),
        });
      } finally {
        setCrawling(false);
      }
    },
    [session.access_token]
  );

  return {
    isCrawling,
    urlInputRef,
    crawlWebsite,
  };
};
