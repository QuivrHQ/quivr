export const mentionTriggers = ["@"] as const;

export type MentionTriggerType = (typeof mentionTriggers)[number];
export type FeedItemSource = "crawl" | "upload";

export type FeedItemCrawlType = {
  source: "crawl";
  url: string;
};

export type FeedItemUploadType = {
  source: "upload";
  file: File;
};

export type FeedItemType = FeedItemCrawlType | FeedItemUploadType;
