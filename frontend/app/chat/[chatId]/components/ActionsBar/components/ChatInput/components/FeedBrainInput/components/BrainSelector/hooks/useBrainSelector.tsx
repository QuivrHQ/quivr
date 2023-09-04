/* eslint-disable max-lines */
import Editor from "@draft-js-plugins/editor";
import {
  defaultSuggestionsFilter,
  MentionData,
} from "@draft-js-plugins/mention";
import { UUID } from "crypto";
import { EditorState, getDefaultKeyBinding } from "draft-js";
import { useCallback, useEffect, useRef, useState } from "react";

import { mentionTriggers } from "@/app/chat/[chatId]/components/ActionsBar/types";
import { getEditorText } from "@/lib/components/MentionInput/utils/getEditorText";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import "@draft-js-plugins/mention/lib/plugin.css";
import "draft-js/dist/Draft.css";

import { useMentionPlugin } from "./helpers/MentionPlugin";
import { useMentionState } from "./helpers/MentionState";
import { MentionTriggerType } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainSelector = () => {
  const {
    currentBrainId,
    currentPromptId,
    setCurrentBrainId,
    setCurrentPromptId,
  } = useBrainContext();

  const {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    suggestions,
  } = useMentionState();

  const { MentionSuggestions, plugins } = useMentionPlugin();

  const [currentTrigger, setCurrentTrigger] = useState<MentionTriggerType>("@");

  const mentionInputRef = useRef<Editor>(null);

  const [open, setOpen] = useState(false);

  const onSearchChange = useCallback(
    ({ trigger, value }: { trigger: MentionTriggerType; value: string }) => {
      setCurrentTrigger(trigger);
      if (currentBrainId !== null) {
        setSuggestions([]);

        return;
      }

      if (value === "") {
        setSuggestions(mentionItems["@"]);

        return;
      }

      setSuggestions(defaultSuggestionsFilter(value, mentionItems, trigger));
    },
    [currentBrainId, mentionItems, setSuggestions]
  );
  const onAddMention = useCallback(
    (mention: MentionData) => {
      if (mention.trigger === "@") {
        setCurrentBrainId(mention.id as UUID);
      }
    },
    [setCurrentBrainId]
  );

  useEffect(() => {
    // Reset editor state when there is no brain selected in order to show placeholder
    if (currentBrainId === null) {
      setEditorState(EditorState.createEmpty());
    }
  }, [currentBrainId, setEditorState]);

  const keyBindingFn = useCallback(
    // eslint-disable-next-line complexity
    (e: React.KeyboardEvent<HTMLDivElement>) => {
      if (mentionTriggers.includes(e.key as MentionTriggerType)) {
        setOpen(true);

        return getDefaultKeyBinding(e);
      }

      if (e.key === "Backspace" || e.key === "Delete") {
        const editorContent = getEditorText(editorState);

        if (editorContent !== "") {
          return getDefaultKeyBinding(e);
        }
        if (currentPromptId !== null) {
          setCurrentPromptId(null);

          return "backspace";
        }
        if (currentBrainId !== null) {
          setCurrentBrainId(null);

          return "backspace";
        }

        return "backspace";
      }

      if (e.key === "ArrowUp" || e.key === "ArrowDown") {
        return undefined;
      }

      return getDefaultKeyBinding(e);
    },
    [
      currentBrainId,
      currentPromptId,
      editorState,
      setCurrentBrainId,
      setCurrentPromptId,
    ]
  );

  const handleEditorChange = useCallback(
    (newEditorState: EditorState) => {
      setEditorState(newEditorState);
    },
    [setEditorState]
  );

  return {
    mentionInputRef,
    plugins,
    MentionSuggestions,
    onSearchChange,
    open,
    suggestions,
    editorState,
    handleEditorChange,
    keyBindingFn,
    currentTrigger,
    setOpen,
    onAddMention,
  };
};
