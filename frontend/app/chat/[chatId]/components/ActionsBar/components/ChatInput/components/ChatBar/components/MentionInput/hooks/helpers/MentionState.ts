/* eslint-disable max-lines */
import { EditorState, Modifier } from "draft-js";
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
    if (currentBrainId === null || mentionItems["@"].length === 0) {
      return;
    }

    const mention = mentionItems["@"].find(
      (item) => item.id === currentBrainId
    );

    if (mention !== undefined) {
      const mentionText = `@${mention.name}`;
      const mentionWithSpace = `${mentionText} `;

      const contentState = editorState.getCurrentContent();
      const plainText = contentState.getPlainText();

      if (plainText.includes(mentionWithSpace)) {
        return;
      }

      const stateWithEntity = contentState.createEntity(
        "mention",
        "IMMUTABLE",
        {
          mention,
        }
      );
      const entityKey = stateWithEntity.getLastCreatedEntityKey();

      const selectionState = editorState.getSelection();
      const updatedContentState = Modifier.insertText(
        contentState,
        selectionState,
        mentionWithSpace,
        undefined,
        entityKey
      );

      const newSelection = selectionState.merge({
        anchorOffset: selectionState.getStartOffset() + mentionWithSpace.length,
        focusOffset: selectionState.getStartOffset() + mentionWithSpace.length,
      });

      const newEditorState = EditorState.forceSelection(
        EditorState.push(editorState, updatedContentState, "insert-characters"),
        newSelection
      );

      setEditorState(newEditorState);
    }
  }, [currentBrainId, mentionItems]);

  return {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    setMentionItems,
    suggestions,
  };
};
