import { useAxios } from "@/lib/hooks";

import { CrawlInputProps, crawlWebsiteUrl } from "./crawl";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useCrawlApi = () => {
  const { axiosInstance } = useAxios();

  return {
    crawlWebsiteUrl: async (props: CrawlInputProps) =>
      crawlWebsiteUrl(props, axiosInstance),
  };
};
