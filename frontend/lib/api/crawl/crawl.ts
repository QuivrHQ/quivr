import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

export type CrawlInputProps = {
  brainId: UUID;
  config: {
    url: string;
    js: boolean;
    depth: number;
    max_pages: number;
    max_time: number;
  };
};

export type CrawlResponse = {
  data: { type: ToastData["variant"]; message: ToastData["text"] };
};

export const crawlWebsiteUrl = async (
  props: CrawlInputProps,
  axiosInstance: AxiosInstance
): Promise<CrawlResponse> =>
  axiosInstance.post(`/crawl?brain_id=${props.brainId}`, props.config);
