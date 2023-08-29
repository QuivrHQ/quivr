import { EditorState, Modifier } from "draft-js";

type MentionUtilsProps = {
  editorState: EditorState;
  setEditorState: (editorState: EditorState) => void;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionUtils = (props: MentionUtilsProps) => {
  const { editorState, setEditorState } = props;

  const removeEntity = (entityKeyToRemove: string): void => {
    const contentState = Modifier.replaceText(
      editorState.getCurrentContent(),
      editorState.getSelection(),
      "",
      editorState.getCurrentInlineStyle(),
      entityKeyToRemove
    );

    const newEditorState = EditorState.set(editorState, {
      currentContent: contentState,
    });

    setEditorState(newEditorState);
  };

  return {
    removeEntity,
  };
};
