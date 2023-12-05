/* eslint-disable max-lines */
import { MentionData } from "@draft-js-plugins/mention";
import { EditorState } from "draft-js";
import { useEffect, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionInputMentionsType } from "../../../../types";
import { mapMinimalBrainToMentionData } from "../../utils/mapMinimalBrainToMentionData";
import { mapPromptToMentionData } from "../../utils/mapPromptToMentionData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionState = () => {
  const { allBrains, publicPrompts } = useBrainContext();

  const [editorState, setEditorState] = useState(EditorState.createEmpty());

  const [mentionItems, setMentionItems] = useState<MentionInputMentionsType>({
    "@": allBrains.map(mapMinimalBrainToMentionData),
    "#": publicPrompts.map(mapPromptToMentionData),
  });

  const [suggestions, setSuggestions] = useState<MentionData[]>([]);

  useEffect(() => {
    setMentionItems({
      ...mentionItems,
      "@": allBrains.map(mapMinimalBrainToMentionData),
    });
  }, [allBrains]);

  useEffect(() => {
    setMentionItems({
      ...mentionItems,
      "#": publicPrompts.map(mapPromptToMentionData),
    });
  }, [publicPrompts]);

  return {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    setMentionItems,
    suggestions,
    publicPrompts,
  };
};
