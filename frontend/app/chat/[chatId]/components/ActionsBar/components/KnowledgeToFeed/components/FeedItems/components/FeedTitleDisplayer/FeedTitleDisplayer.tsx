import { useState } from "react";

import { enhanceUrlDisplay } from "./utils/enhanceUrlDisplay";
import { removeFileExtension } from "./utils/removeFileExtension";

type FeedTitleDisplayerProps = {
  title: string;
  truncate?: boolean;
};

export const FeedTitleDisplayer = ({
  title,
  truncate = false,
}: FeedTitleDisplayerProps): JSX.Element => {
  const [showFullUrl, setShowFullUrl] = useState(false);

  const toggleShowFullUrl = () => {
    setShowFullUrl(!showFullUrl);
  };

  if (truncate) {
    return (
      <div className="overflow-hidden">
        <span className="cursor-pointer" onClick={toggleShowFullUrl}>
          <p className={showFullUrl ? "" : "truncate"}>
            {removeFileExtension(title)}
          </p>
        </span>
      </div>
    );
  }

  return (
    <div>
      <span className="cursor-pointer" onClick={toggleShowFullUrl}>
        {showFullUrl ? title : enhanceUrlDisplay(title)}
      </span>
    </div>
  );
};
