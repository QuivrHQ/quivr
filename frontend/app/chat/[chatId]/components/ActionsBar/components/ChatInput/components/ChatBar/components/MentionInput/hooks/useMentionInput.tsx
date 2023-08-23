/* eslint-disable max-lines */
import Editor from "@draft-js-plugins/editor";
import {
  defaultSuggestionsFilter,
  MentionData,
} from "@draft-js-plugins/mention";
import { UUID } from "crypto";
import { EditorState, getDefaultKeyBinding } from "draft-js";
import { useCallback, useEffect, useRef, useState } from "react";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import "@draft-js-plugins/mention/lib/plugin.css";
import "draft-js/dist/Draft.css";


import { useMentionPlugin } from "./helpers/MentionPlugin";
import { useMentionState } from "./helpers/MentionState";
import { useMentionUtils } from "./helpers/MentionUtils";
import { mapMinimalBrainToMentionData } from "../utils/mapMinimalBrainToMentionData";

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
    allBrains,
    currentBrainId,
    currentPromptId,
    setCurrentBrainId,
    setCurrentPromptId,
  } = useBrainContext();

  const {
    editorState,
    setEditorState,
    setMentionItems,
    mentionItems,
    setSuggestions,
    suggestions,
    getEditorCurrentMentions,
    getEditorTextWithoutMentions,
    publicPrompts,
  } = useMentionState();

  const { removeMention, insertMention } = useMentionUtils({
    editorState,
    setEditorState,
  });

  const { BrainMentionSuggestions, PromptMentionSuggestions, plugins } =
    useMentionPlugin({
      removeMention,
    });

  const mentionInputRef = useRef<Editor>(null);

  const [selectedBrainAddedOnload, setSelectedBrainAddedOnload] =
    useState(false);

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

  const insertCurrentBrainAsMention = (): void => {
    const mention = mentionItems["@"].find(
      (item) => item.id === currentBrainId
    );

    if (mention !== undefined) {
      insertMention(mention);
    }
  };
  const insertCurrentPromptAsMention = (): void => {
    const mention = mentionItems["#"].find(
      (item) => item.id === currentPromptId
    );

    if (mention !== undefined) {
      insertMention(mention);
    }
  };

  const resetEditorContent = () => {
    const currentMentions = getEditorCurrentMentions();
    let newEditorState = EditorState.createEmpty();
    currentMentions.forEach((mention) => {
      const correspondingMention = mentionItems[
        mention.trigger as MentionTriggerType
      ].find((item) => item.name === mention.name);

      if (correspondingMention !== undefined) {
        newEditorState = insertMention(correspondingMention, newEditorState);
      }
    });

    setEditorState(newEditorState);
  };

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
    const currentMessage = getEditorTextWithoutMentions(newEditorState);
    setMessage(currentMessage);
  };

  useEffect(() => {
    if (message === "") {
      resetEditorContent();
    }
  }, [message]);

  useEffect(() => {
    setMentionItems({
      ...mentionItems,
      "@": allBrains.map(mapMinimalBrainToMentionData),
    });
  }, [allBrains]);

  useEffect(() => {
    if (
      selectedBrainAddedOnload ||
      mentionItems["@"].length === 0 ||
      currentBrainId === null
    ) {
      return;
    }

    insertCurrentBrainAsMention();

    setSelectedBrainAddedOnload(true);
  }, [currentBrainId, mentionItems]);

  useEffect(() => {
    const contentState = editorState.getCurrentContent();
    const plainText = contentState.getPlainText();

    if (plainText === "") {
      if (currentBrainId !== null) {
        insertCurrentBrainAsMention();
      }
      if (currentPromptId !== null) {
        insertCurrentPromptAsMention();
      }
    }
  }, [editorState]);

  return {
    mentionInputRef,
    plugins,
    BrainMentionSuggestions,
    PromptMentionSuggestions,
    onOpenChange,
    onSearchChange,
    open,
    suggestions,
    onAddMention,
    editorState,
    insertCurrentBrainAsMention,
    handleEditorChange,
    keyBindingFn,
    publicPrompts,
  };
};
