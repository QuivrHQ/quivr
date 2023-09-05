import { Fragment } from "react";
import { IoMdCloseCircle } from "react-icons/io";
import { MdLink } from "react-icons/md";

import { UrlDisplay } from "./components";
import { FeedItemType } from "../../types";

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
      {contents.map((item, index) => (
        <div
          key={item.url}
          className="relative bg-gray-100 p-4 rounded-lg shadow-sm"
        >
          <IoMdCloseCircle
            className="absolute top-2 right-2 cursor-pointer text-gray-400 text-2xl"
            onClick={() => removeContent(index)}
          />
          <div className="flex items-center">
            <MdLink className="mr-2 text-2xl" />
            <UrlDisplay url={item.url} />
          </div>
        </div>
      ))}
    </div>
  );
};
