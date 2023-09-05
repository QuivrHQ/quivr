import { useState } from "react";

import { KnowledgeToFeed } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeToFeed = () => {
  const [contents, setContents] = useState<KnowledgeToFeed[]>([]);

  const addContent = (content: KnowledgeToFeed) => {
    setContents((prevContents) => [...prevContents, content]);
  };
  const removeContent = (index: number) => {
    setContents((prevContents) => prevContents.filter((_, i) => i !== index));
  };

  return {
    addContent,
    contents,
    setContents,
    removeContent,
  };
};
