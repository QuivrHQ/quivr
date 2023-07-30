/* eslint-disable */
import { useCallback, useRef, useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useAxios, useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { UUID } from "crypto";
import { isValidUrl } from "../helpers/isValidUrl";

export const useCrawler = () => {
  const [isCrawling, setCrawling] = useState(false);
  const urlInputRef = useRef<HTMLInputElement | null>(null);
  const { session } = useSupabase();
  const { publish } = useToast();
  const { axiosInstance } = useAxios();
  const { track } = useEventTracking();

  if (session === null) {
    redirectToLogin();
  }

  const crawlWebsite = useCallback(
    async (brainId: UUID | undefined) => {
      // Validate URL
      const url = urlInputRef.current ? urlInputRef.current.value : null;

      if (!url || !isValidUrl(url)) {
        void track("URL_INVALID");

        publish({
          variant: "danger",
          text: "Invalid URL",
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
          const response = await axiosInstance.post(
            `/crawl?brain_id=${brainId}`,
            config
          );

          publish({
            variant: response.data.type,
            text: response.data.message,
          });
        }
      } catch (error: unknown) {
        publish({
          variant: "danger",
          text: "Failed to crawl website: " + JSON.stringify(error),
        });
      } finally {
        setCrawling(false);
      }
    },
    [session.access_token, publish]
  );

  return {
    isCrawling,
    urlInputRef,

    crawlWebsite,
  };
};
