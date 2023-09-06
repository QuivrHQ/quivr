export type FeedItemSource = "crawl" | "upload";

type FeedItemCrawlType = {
  source: "crawl";
  url: string;
};

export type FeedItemUploadType = {
  source: "upload";
  file: File;
};

export type FeedItemType = FeedItemCrawlType | FeedItemUploadType;
