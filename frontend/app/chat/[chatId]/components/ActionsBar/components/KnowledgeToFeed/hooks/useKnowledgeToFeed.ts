import { useState } from "react";

import { FeedItemType, FeedItemUploadType } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeToFeed = () => {
  const [contents, setContents] = useState<FeedItemType[]>([]);

  const addContent = (content: FeedItemType) => {
    setContents((prevContents) => [...prevContents, content]);
  };
  const removeContent = (index: number) => {
    setContents((prevContents) => prevContents.filter((_, i) => i !== index));
  };

  const files: File[] = (
    contents.filter((c) => c.source === "upload") as FeedItemUploadType[]
  ).map((c) => c.file);

  return {
    addContent,
    contents,
    setContents,
    removeContent,
    files,
  };
};
