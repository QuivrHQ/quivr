import { MentionData } from "@draft-js-plugins/mention";
import { EditorState, Modifier } from "draft-js";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

type MentionUtilsProps = {
  editorState: EditorState;
  setEditorState: (editorState: EditorState) => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionUtils = (props: MentionUtilsProps) => {
  const { editorState, setEditorState } = props;
  const { setCurrentBrainId } = useBrainContext();

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

  const insertMention = (
    mention: MentionData,
    mentionWithSpace = " "
  ): EditorState => {
    const contentState = editorState.getCurrentContent();
    const selectionState = editorState.getSelection();

    const stateWithEntity = contentState.createEntity("mention", "IMMUTABLE", {
      mention,
    });
    const entityKey = stateWithEntity.getLastCreatedEntityKey();

    const newContentState = Modifier.insertText(
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
      EditorState.push(editorState, newContentState, "insert-characters"),
      newSelection
    );

    return newEditorState;
  };

  return {
    removeMention,
    insertMention,
  };
};
