import { IoMdCloseCircle } from "react-icons/io";
import { MdLink } from "react-icons/md";

import { FeedTitleDisplayer } from "./FeedTitleDisplayer";

type CrawlFeedItemProps = {
  url: string;
  onRemove: () => void;
};
export const CrawlFeedItem = ({
  url,
  onRemove,
}: CrawlFeedItemProps): JSX.Element => {
  return (
    <div className="relative bg-gray-100 p-4 rounded-lg shadow-sm">
      <IoMdCloseCircle
        className="absolute top-2 right-2 cursor-pointer text-gray-400 text-2xl"
        onClick={onRemove}
      />
      <div className="flex items-center">
        <MdLink className="mr-2 text-2xl" />
        <FeedTitleDisplayer title={url} />
      </div>
    </div>
  );
};
