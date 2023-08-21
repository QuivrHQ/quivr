import { EditorState } from "draft-js";
import { useEffect, useState } from "react";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionInputMentionsType, TriggerMap } from "../../../../types";
import { mapMinimalBrainToMentionData } from "../../utils/mapMinimalBrainToMentionData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionState = () => {
  const { allBrains } = useBrainContext();
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

  const getEditorCurrentMentions = (): TriggerMap[] => {
    const contentState = editorState.getCurrentContent();
    const plainText = contentState.getPlainText();
    const mentionTriggers = Object.keys(mentionItems);

    const mentionTexts: TriggerMap[] = [];

    mentionTriggers.forEach((trigger) => {
      if (trigger === "@") {
        mentionItems["@"].forEach((item) => {
          const mentionText = `${trigger}${item.name}`;
          if (plainText.includes(mentionText)) {
            mentionTexts.push({
              trigger: trigger as MentionTriggerType,
              content: item.name,
            });
          }
        });
      }
    });

    return mentionTexts;
  };

  const getEditorTextWithoutMentions = (
    editorCurrentState: EditorState
  ): string => {
    const contentState = editorCurrentState.getCurrentContent();
    let plainText = contentState.getPlainText();
    Object.keys(mentionItems).forEach((trigger) => {
      if (trigger === "@") {
        mentionItems[trigger].forEach((item) => {
          const regex = new RegExp(`${trigger}${item.name}`, "g");
          plainText = plainText.replace(regex, "");
        });
      }
    });

    return plainText;
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

  return {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    setMentionItems,
    suggestions,
    getEditorCurrentMentions,
    getEditorTextWithoutMentions,
  };
};
