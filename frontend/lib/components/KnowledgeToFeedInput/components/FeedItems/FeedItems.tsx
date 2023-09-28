import { Fragment } from "react";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import { CrawlFeedItem } from "./components/CrawlFeedItem";
import { FileFeedItem } from "./components/FileFeedItem";

export const FeedItems = (): JSX.Element => {
  const { knowledgeToFeed, removeKnowledgeToFeed } =
    useKnowledgeToFeedContext();
  if (knowledgeToFeed.length === 0) {
    return <Fragment />;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mt-1 bg-white py-6 overflow-scroll">
      {knowledgeToFeed.map((item, index) =>
        item.source === "crawl" ? (
          <CrawlFeedItem
            key={item.url}
            url={item.url}
            onRemove={() => removeKnowledgeToFeed(index)}
          />
        ) : (
          <FileFeedItem
            key={item.file.name}
            file={item.file}
            onRemove={() => removeKnowledgeToFeed(index)}
          />
        )
      )}
    </div>
  );
};
