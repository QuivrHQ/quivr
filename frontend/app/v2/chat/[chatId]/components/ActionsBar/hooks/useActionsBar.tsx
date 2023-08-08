import { useState } from "react";

import { MentionType } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useActionsBar = () => {
  const [value, setValue] = useState("");
  const [mentions, setMentions] = useState<MentionType[]>([]); // Store the list of mentions

  const handleChange = (newPlainTextValue: string) => {
    setValue(newPlainTextValue);
  };

  const handleAddMention: (id: string, display: string) => void = (
    id,
    display
  ) => {
    setMentions([...mentions, { id, display }]);
  };

  const handleRemoveMention = (id: string) => {
    const updatedMentions = mentions.filter((m) => m.id !== id);
    setMentions(updatedMentions);
  };

  return {
    mentions,
    handleAddMention,
    handleRemoveMention,
    handleChange,
    value,
  };
};
