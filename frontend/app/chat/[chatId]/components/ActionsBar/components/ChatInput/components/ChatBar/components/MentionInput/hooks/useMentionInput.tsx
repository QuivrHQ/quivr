/* eslint-disable max-lines */
import Editor from "@draft-js-plugins/editor";
import createMentionPlugin, {
  defaultSuggestionsFilter,
  MentionData,
} from "@draft-js-plugins/mention";
import { UUID } from "crypto";
import { EditorState, Modifier } from "draft-js";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainMentionsList } from "../../../types";
import { BrainMentionItem } from "../../BrainMentionItem";
import { mapToMentionData } from "../utils/mapToMentionData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionInput = () => {
  const { allBrains } = useBrainContext();

  const [selectedBrainAddedOnload, setSelectedBrainAddedOnload] =
    useState(false);

  const { setCurrentBrainId, currentBrainId } = useBrainContext();
  const [editorState, setEditorState] = useState(() =>
    EditorState.createEmpty()
  );

  const [open, setOpen] = useState(false);

  const [mentionItems, setMentionItems] = useState<BrainMentionsList>({
    "@": allBrains.map((brain) => ({ ...brain, value: brain.name })),
  });

  const [suggestions, setSuggestions] = useState(
    mapToMentionData(mentionItems["@"])
  );

  const mentionInputRef = useRef<Editor>(null);

  const onAddMention = (mention: MentionData) => {
    setCurrentBrainId(mention.id as UUID);
  };

  const removeMention = (entityKeyToRemove: string): void => {
    const contentState = editorState.getCurrentContent();
    const entity = contentState.getEntity(entityKeyToRemove);

    if (entity.getType() === "mention") {
      const newContentState = contentState.replaceEntityData(
        entityKeyToRemove,
        {}
      );

      const newEditorState = EditorState.push(
        editorState,
        newContentState,
        "apply-entity"
      );

      setEditorState(newEditorState);
      setCurrentBrainId(null);
    }
  };

  const { MentionSuggestions, plugins } = useMemo(() => {
    const mentionPlugin = createMentionPlugin({
      mentionComponent: ({ entityKey, mention: { name } }) => (
        <BrainMentionItem
          text={name + "" + entityKey}
          onRemove={() => removeMention(entityKey)}
        />
      ),

      popperOptions: {
        placement: "top-end",
      },
    });
    const { MentionSuggestions: coreMentionSuggestions } = mentionPlugin;
    const corePlugins = [mentionPlugin];

    return { plugins: corePlugins, MentionSuggestions: coreMentionSuggestions };
  }, []);

  const onOpenChange = useCallback((_open: boolean) => {
    setOpen(_open);
  }, []);

  const onSearchChange = useCallback(
    ({ trigger, value }: { trigger: string; value: string }) => {
      setSuggestions(
        defaultSuggestionsFilter(
          value,
          currentBrainId !== null ? [] : mapToMentionData(mentionItems["@"]),
          trigger
        )
      );
    },
    [mentionItems, currentBrainId]
  );

  useEffect(() => {
    setSuggestions(mapToMentionData(mentionItems["@"]));
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

    if (mention !== undefined) {
      const mentionText = `@${mention.name}`;
      const mentionWithSpace = `${mentionText} `; // Add white space after the mention

      // Check if the mention with white space is already in the editor's content
      const contentState = editorState.getCurrentContent();
      const plainText = contentState.getPlainText();

      if (plainText.includes(mentionWithSpace)) {
        return; // Mention with white space already in content, no need to add it again
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

      // Calculate the new selection position after inserting the mention with white space
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
    setSelectedBrainAddedOnload(true);
  }, [currentBrainId, mentionItems]);

  return {
    mentionInputRef,
    editorState,
    setEditorState,
    plugins,
    MentionSuggestions,
    onOpenChange,
    onSearchChange,
    open,
    suggestions,
    onAddMention,
  };
};
