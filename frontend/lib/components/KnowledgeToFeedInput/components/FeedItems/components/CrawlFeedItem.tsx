import { IoMdCloseCircle } from "react-icons/io";
import { MdLink } from "react-icons/md";

import { FeedTitleDisplayer } from "./FeedTitleDisplayer";
import { StyledFeedItemDiv } from "../styles/StyledFeedItemDiv";

type CrawlFeedItemProps = {
  url: string;
  onRemove: () => void;
};
export const CrawlFeedItem = ({
  url,
  onRemove,
}: CrawlFeedItemProps): JSX.Element => {
  return (
    <StyledFeedItemDiv>
      <div className="flex flex-1 items-center">
        <div>
          <MdLink className="mr-2 text-2xl" />
        </div>
        <div className="flex flex-1">
          <FeedTitleDisplayer title={url} />
        </div>
      </div>
      <IoMdCloseCircle
        className="cursor-pointer text-gray-400 text-lg"
        onClick={onRemove}
      />
    </StyledFeedItemDiv>
  );
};
