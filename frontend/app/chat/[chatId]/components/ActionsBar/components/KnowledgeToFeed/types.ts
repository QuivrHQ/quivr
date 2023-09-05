export type FeedItemSource = "crawl" | "upload";

export type FeedItemType = {
  source: FeedItemSource;
  url: string;
};
