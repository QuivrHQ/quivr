import { useState } from "react";

import { cn } from "@/lib/utils";

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
      <div>
        <p
          onClick={toggleShowFullUrl}
          className={cn("cursor-pointer", showFullUrl ? "" : "line-clamp-1")}
        >
          {removeFileExtension(title)}
        </p>
      </div>
    );
  }

  return (
    <div>
      <p
        className={cn("cursor-pointer", `${showFullUrl ? "" : "line-clamp-1"}`)}
        onClick={toggleShowFullUrl}
      >
        {showFullUrl ? title : enhanceUrlDisplay(title)}
      </p>
    </div>
  );
};
