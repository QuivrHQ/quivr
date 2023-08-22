/* eslint-disable max-lines */
import { MentionData } from "@draft-js-plugins/mention";
import { EditorState } from "draft-js";
import { useEffect, useState } from "react";

import {
  mentionTriggers,
  MentionTriggerType,
} from "@/app/chat/[chatId]/components/ActionsBar/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionInputMentionsType, TriggerMap } from "../../../../types";
import { mapMinimalBrainToMentionData } from "../../utils/mapMinimalBrainToMentionData";
import { mapPromptToMentionData } from "../../utils/mapPromptToMentionData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionState = () => {
  const { allBrains, publicPrompts } = useBrainContext();

  const [editorState, legacySetEditorState] = useState(() =>
    EditorState.createEmpty()
  );

  const [mentionItems, setMentionItems] = useState<MentionInputMentionsType>({
    "@": allBrains.map(mapMinimalBrainToMentionData),
    "#": publicPrompts.map(mapPromptToMentionData),
  });

  const [suggestions, setSuggestions] = useState<MentionData[]>([]);

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

    const mentionTexts: TriggerMap[] = [];

    mentionTriggers.forEach((trigger) => {
      mentionItems[trigger].forEach((item) => {
        if (plainText.includes(item.name)) {
          mentionTexts.push({
            trigger: trigger,
            content: item.name,
          });
        }
      });
    });

    return mentionTexts;
  };

  const getEditorTextWithoutMentions = (
    editorCurrentState: EditorState
  ): string => {
    const contentState = editorCurrentState.getCurrentContent();
    let plainText = contentState.getPlainText();
    (Object.keys(mentionItems) as MentionTriggerType[]).forEach((trigger) => {
      if (mentionTriggers.includes(trigger)) {
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
    getEditorCurrentMentions,
    getEditorTextWithoutMentions,
    publicPrompts,
  };
};
