import { MdLink } from "react-icons/md";

import { FeedItemType } from "../../types";

type FeedItemsProps = {
  contents: FeedItemType[];
};

export const FeedItems = ({ contents }: FeedItemsProps): JSX.Element => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 mt-5 shadow-md shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-6">
      {contents.map((item) => (
        <div
          key={item.url}
          className="bg-gray-100 p-4 rounded-lg shadow-xs flex items-center"
        >
          <MdLink className="text-blue-500 mr-2" />
          <span className="text-blue-500 hover:underline">{item.url}</span>
        </div>
      ))}
    </div>
  );
};
