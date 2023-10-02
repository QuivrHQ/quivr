import { IoMdCloseCircle } from "react-icons/io";

import { getFileIcon } from "@/lib/helpers/getFileIcon";

import { FeedTitleDisplayer } from "./FeedTitleDisplayer";
import { StyledFeedItemDiv } from "../styles/StyledFeedItemDiv";

type FileFeedItemProps = {
  file: File;
  onRemove: () => void;
};

export const FileFeedItem = ({
  file,
  onRemove,
}: FileFeedItemProps): JSX.Element => {
  const icon = getFileIcon(file.name);

  return (
    <StyledFeedItemDiv>
      <div className="flex flex-1 overflow-hidden items-center gap-1">
        <div>{icon}</div>
        <div className="flex flex-1">
          <FeedTitleDisplayer title={file.name} />
        </div>
      </div>
      <div>
        <IoMdCloseCircle
          className="cursor-pointer text-gray-400 text-lg"
          onClick={onRemove}
        />
      </div>
    </StyledFeedItemDiv>
  );
};
