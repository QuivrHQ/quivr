/* eslint-disable max-lines */
import Editor from "@draft-js-plugins/editor";
import {
  defaultSuggestionsFilter,
  MentionData,
} from "@draft-js-plugins/mention";
import { UUID } from "crypto";
import { EditorState, getDefaultKeyBinding } from "draft-js";
import { useCallback, useEffect, useRef, useState } from "react";

import {
  mentionTriggers,
  MentionTriggerType,
} from "@/app/chat/[chatId]/components/ActionsBar/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useJune } from "@/services/analytics/june/useJune";
import "@draft-js-plugins/mention/lib/plugin.css";
import "draft-js/dist/Draft.css";

import { useMentionPlugin } from "./helpers/MentionPlugin";
import { useMentionState } from "./helpers/MentionState";
import { getEditorText } from "./helpers/getEditorText";

type UseMentionInputProps = {
  message: string;
  onSubmit: () => void;
  setMessage: (text: string) => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionInput = ({
  message,
  onSubmit,
  setMessage,
}: UseMentionInputProps) => {
  const {
    currentBrainId,
    currentPromptId,
    setCurrentBrainId,
    setCurrentPromptId,
  } = useBrainContext();

  const analytics = useJune();
  const {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    suggestions,
    publicPrompts,
  } = useMentionState();

  const { MentionSuggestions, plugins } = useMentionPlugin();

  const [currentTrigger, setCurrentTrigger] = useState<MentionTriggerType>("@");

  const mentionInputRef = useRef<Editor>(null);

  const [open, setOpen] = useState(false);

  const onAddMention = useCallback(
    (mention: MentionData) => {
      if (mention.trigger === "#") {
        void analytics?.track("CHANGE_PROMPT");
        setCurrentPromptId(mention.id as UUID);
      }

      if (mention.trigger === "@") {
        void analytics?.track("CHANGE_BRAIN");
        setCurrentBrainId(mention.id as UUID);
      }
    },
    [analytics, setCurrentBrainId, setCurrentPromptId]
  );

  const onSearchChange = useCallback(
    ({ trigger, value }: { trigger: MentionTriggerType; value: string }) => {
      setCurrentTrigger(trigger);
      if (trigger === "@") {
        if (currentBrainId !== null) {
          setSuggestions([]);

          return;
        }

        if (value === "") {
          setSuggestions(mentionItems["@"]);

          return;
        }
      }
      if (trigger === "#") {
        if (currentPromptId !== null) {
          setSuggestions([]);

          return;
        }
        if (value === "") {
          setSuggestions(mentionItems["#"]);

          return;
        }
      }

      setSuggestions(defaultSuggestionsFilter(value, mentionItems, trigger));
    },
    [currentBrainId, currentPromptId, mentionItems, setSuggestions]
  );

  const resetEditorContent = useCallback(() => {
    setEditorState(EditorState.createEmpty());
  }, [setEditorState]);

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

      if (e.key === "Enter" && !e.shiftKey) {
        onSubmit();

        return "submit";
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
      onSubmit,
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

  useEffect(() => {
    const currentMessage = getEditorText(editorState);

    if (currentMessage !== "") {
      setMessage(currentMessage);
    }
  }, [editorState, setMessage]);

  useEffect(() => {
    if (message === "") {
      resetEditorContent();
    }
  }, [message, resetEditorContent]);

  return {
    mentionInputRef,
    plugins,
    MentionSuggestions,
    onSearchChange,
    open,
    suggestions,
    onAddMention,
    editorState,
    handleEditorChange,
    keyBindingFn,
    publicPrompts,
    currentTrigger,
    setOpen,
  };
};
