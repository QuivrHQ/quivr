import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

export type CrawlInputProps = {
  brainId: UUID;
  chat_id?: UUID;
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
): Promise<CrawlResponse> => {
  let crawlUrl = `/crawl?brain_id=${props.brainId}`;

  if (props.chat_id !== undefined) {
    crawlUrl = crawlUrl.concat(`&chat_id=${props.chat_id}`);
  }

  return axiosInstance.post(crawlUrl, props.config);
};
