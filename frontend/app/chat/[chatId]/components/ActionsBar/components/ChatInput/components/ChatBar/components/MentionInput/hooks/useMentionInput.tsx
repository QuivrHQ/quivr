/* eslint-disable max-lines */
import Editor from "@draft-js-plugins/editor";
import {
  defaultSuggestionsFilter,
  MentionData,
} from "@draft-js-plugins/mention";
import { UUID } from "crypto";
import { EditorState, getDefaultKeyBinding } from "draft-js";
import { useCallback, useEffect, useRef, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import "@draft-js-plugins/mention/lib/plugin.css";
import "draft-js/dist/Draft.css";

import { useMentionPlugin } from "./helpers/MentionPlugin";
import { useMentionState } from "./helpers/MentionState";
import { useMentionUtils } from "./helpers/MentionUtils";
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

  const {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    suggestions,
    publicPrompts,
  } = useMentionState();

  const { removeEntity } = useMentionUtils({
    editorState,
    setEditorState,
  });

  const { MentionSuggestions, plugins } = useMentionPlugin();

  const mentionInputRef = useRef<Editor>(null);

  const [open, setOpen] = useState(false);

  const onOpenChange = useCallback((_open: boolean) => {
    setOpen(_open);
  }, []);

  const onAddMention = (mention: MentionData) => {
    if (mention.trigger === "#") {
      setCurrentPromptId(mention.id as UUID);
    }

    if (mention.trigger === "@") {
      setCurrentBrainId(mention.id as UUID);
    }

    const lastEntityKey = editorState
      .getCurrentContent()
      .getLastCreatedEntityKey();
    removeEntity(lastEntityKey);
  };

  const onSearchChange = ({
    trigger,
    value,
  }: {
    trigger: string;
    value: string;
  }) => {
    if (currentBrainId !== null && trigger === "@") {
      setSuggestions([]);

      return;
    }
    if (currentPromptId !== null && trigger === "#") {
      setSuggestions([]);

      return;
    }

    setSuggestions(defaultSuggestionsFilter(value, mentionItems, trigger));
  };

  const resetEditorContent = useCallback(() => {
    setEditorState(EditorState.createEmpty());
  }, [setEditorState]);

  const keyBindingFn = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      onSubmit();

      return "submit";
    }

    if (e.key === "ArrowUp" || e.key === "ArrowDown") {
      return undefined;
    }

    return getDefaultKeyBinding(e);
  };

  const handleEditorChange = (newEditorState: EditorState) => {
    setEditorState(newEditorState);
  };

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
    onOpenChange,
    onSearchChange,
    open,
    suggestions,
    onAddMention,
    editorState,
    handleEditorChange,
    keyBindingFn,
    publicPrompts,
  };
};
