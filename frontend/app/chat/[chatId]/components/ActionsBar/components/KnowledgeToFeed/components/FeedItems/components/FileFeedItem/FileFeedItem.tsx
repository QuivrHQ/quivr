import { IoMdCloseCircle } from "react-icons/io";

import { getFileIcon } from "./helpers/getFileIcon";
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
    <div className="relative bg-gray-100 p-4 rounded-lg shadow-sm">
      <IoMdCloseCircle
        className="absolute top-2 right-2 cursor-pointer text-gray-400 text-2xl"
        onClick={onRemove}
      />
      <div className="flex items-center">
        {icon}
        <FeedTitleDisplayer title={file.name} truncate />
      </div>
    </div>
  );
};
