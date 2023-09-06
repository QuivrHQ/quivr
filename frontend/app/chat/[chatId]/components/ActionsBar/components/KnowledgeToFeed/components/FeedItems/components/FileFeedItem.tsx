import { IoMdCloseCircle } from "react-icons/io";
import { MdLink } from "react-icons/md";

import { UrlDisplay } from "./UrlDisplay";

type FileFeedItemProps = {
  file: File;
  onRemove: () => void;
};

export const FileFeedItem = ({
  file,
  onRemove,
}: FileFeedItemProps): JSX.Element => {
  return (
    <div className="relative bg-gray-100 p-4 rounded-lg shadow-sm">
      <IoMdCloseCircle
        className="absolute top-2 right-2 cursor-pointer text-gray-400 text-2xl"
        onClick={onRemove}
      />
      <div className="flex items-center">
        <MdLink className="mr-2 text-2xl" />
        <UrlDisplay url={file.name} />
      </div>
    </div>
  );
};
