import { useState } from "react";

import { enhanceUrlDisplay } from "./utils/enhanceUrlDisplay";

type UrlDisplayProps = {
  url: string;
};

export const UrlDisplay = ({ url }: UrlDisplayProps): JSX.Element => {
  const [showFullUrl, setShowFullUrl] = useState(false);

  const toggleShowFullUrl = () => {
    setShowFullUrl(!showFullUrl);
  };

  return (
    <div>
      <span className="cursor-pointer" onClick={toggleShowFullUrl}>
        {showFullUrl ? url : enhanceUrlDisplay(url)}
      </span>
    </div>
  );
};
