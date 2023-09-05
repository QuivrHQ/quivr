import { useState } from "react";

import { FeedItemType } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeed = () => {
  const [contents, setContents] = useState<FeedItemType[]>([]);

  const addContent = (content: FeedItemType) => {
    setContents((prevContents) => [...prevContents, content]);
  };

  return {
    addContent,
    contents,
    setContents,
  };
};
