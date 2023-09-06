import { Fragment } from "react";

import { CrawlFeedItem } from "./components/CrawlFeedItem";
import { FileFeedItem } from "./components/FileFeedItem/FileFeedItem";
import { FeedItemType } from "../../../../types";

type FeedItemsProps = {
  contents: FeedItemType[];
  removeContent: (index: number) => void;
};

export const FeedItems = ({
  contents,
  removeContent,
}: FeedItemsProps): JSX.Element => {
  if (contents.length === 0) {
    return <Fragment />;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 mt-5 shadow-md shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
      {contents.map((item, index) =>
        item.source === "crawl" ? (
          <CrawlFeedItem
            key={item.url}
            url={item.url}
            onRemove={() => removeContent(index)}
          />
        ) : (
          <FileFeedItem
            key={item.file.name}
            file={item.file}
            onRemove={() => removeContent(index)}
          />
        )
      )}
    </div>
  );
};
