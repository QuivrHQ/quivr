import { IoMdCloseCircle } from "react-icons/io";

import { getFileIcon } from "@/lib/helpers/getFileIcon";

import { StyledFeedItemDiv } from "../../styles/StyledFeedItemDiv";
import { FeedTitleDisplayer } from "../FeedTitleDisplayer";

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
      <div className="flex flex-1 overflow-auto items-center gap-1">
        {icon}
        <FeedTitleDisplayer title={file.name} truncate />
      </div>
      <IoMdCloseCircle
        className="cursor-pointer text-gray-400 text-lg"
        onClick={onRemove}
      />
    </StyledFeedItemDiv>
  );
};
