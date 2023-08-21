/* eslint-disable max-lines */
import { EditorState } from "draft-js";
import { useEffect, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionInputMentionsType } from "../../../../types";
import { mapMinimalBrainToMentionData } from "../../utils/mapMinimalBrainToMentionData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionState = () => {
  const { allBrains, currentBrainId } = useBrainContext();
  const [editorState, legacySetEditorState] = useState(() =>
    EditorState.createEmpty()
  );

  const [mentionItems, setMentionItems] = useState<MentionInputMentionsType>({
    "@": allBrains.map((brain) => ({ ...brain, value: brain.name })),
  });

  const [suggestions, setSuggestions] = useState(
    mapMinimalBrainToMentionData(mentionItems["@"])
  );

  const setEditorState = (newState: EditorState) => {
    const currentSelection = newState.getSelection();
    const stateWithContentAndSelection = EditorState.forceSelection(
      newState,
      currentSelection
    );

    legacySetEditorState(stateWithContentAndSelection);
  };

  useEffect(() => {
    setMentionItems({
      ...mentionItems,
      "@": [
        ...allBrains.map((brain) => ({
          ...brain,
          value: brain.name,
        })),
      ],
    });
  }, [allBrains]);

  useEffect(() => {
    console.log("changed");
    console.log({ editorState });
  }, [editorState]);

  return {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    setMentionItems,
    suggestions,
  };
};
