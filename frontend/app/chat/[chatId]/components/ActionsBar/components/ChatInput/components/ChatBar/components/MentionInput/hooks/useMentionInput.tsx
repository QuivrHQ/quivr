/* eslint-disable max-lines */
import Editor from "@draft-js-plugins/editor";
import {
  defaultSuggestionsFilter,
  MentionData,
} from "@draft-js-plugins/mention";
import { UUID } from "crypto";
import { useCallback, useEffect, useRef, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useMentionPlugin } from "./helpers/MentionPlugin";
import { useMentionState } from "./helpers/MentionState";
import { useMentionUtils } from "./helpers/MentionUtils";
import { mapMinimalBrainToMentionData } from "../utils/mapMinimalBrainToMentionData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionInput = () => {
  const { allBrains, currentBrainId, setCurrentBrainId } = useBrainContext();

  const {
    editorState,
    setEditorState,
    setMentionItems,
    mentionItems,
    setSuggestions,
    suggestions,
  } = useMentionState();

  const { removeMention, insertMention } = useMentionUtils({
    editorState,
    setEditorState,
  });

  const { MentionSuggestions, plugins } = useMentionPlugin({
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
    setCurrentBrainId(mention.id as UUID);
  };

  const onSearchChange = useCallback(
    ({ trigger, value }: { trigger: string; value: string }) => {
      setSuggestions(
        defaultSuggestionsFilter(
          value,
          currentBrainId !== null
            ? []
            : mapMinimalBrainToMentionData(mentionItems["@"]),
          trigger
        )
      );
    },
    [mentionItems, currentBrainId]
  );

  useEffect(() => {
    setSuggestions(mapMinimalBrainToMentionData(mentionItems["@"]));
  }, [mentionItems]);

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
    if (selectedBrainAddedOnload) {
      return;
    }

    if (currentBrainId === null || mentionItems["@"].length === 0) {
      return;
    }

    const mention = mentionItems["@"].find(
      (item) => item.id === currentBrainId
    );

    if (mention === undefined) {
      return;
    }

    insertMention({
      id: currentBrainId,
      name: mention.name,
    });

    setSelectedBrainAddedOnload(true);
  }, [currentBrainId, mentionItems]);

  return {
    mentionInputRef,
    plugins,
    MentionSuggestions,
    onOpenChange,
    onSearchChange,
    open,
    suggestions,
    onAddMention,
    setEditorState,
    editorState,
  };
};
