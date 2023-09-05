export type KnowledgeToFeedSource = "crawl" | "upload";

export type KnowledgeToFeed = {
  source: KnowledgeToFeedSource;
  url: string;
};
