import { addMention, MentionData } from "@draft-js-plugins/mention";
import { EditorState } from "draft-js";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";
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
    trigger: MentionTriggerType,
    customEditorState?: EditorState
  ): EditorState => {
    const editorStateWithMention = addMention(
      customEditorState ?? editorState,
      mention,
      trigger,
      trigger,
      "MUTABLE"
    );

    setEditorState(editorStateWithMention);

    return editorStateWithMention;
  };

  return {
    removeMention,
    insertMention,
  };
};
