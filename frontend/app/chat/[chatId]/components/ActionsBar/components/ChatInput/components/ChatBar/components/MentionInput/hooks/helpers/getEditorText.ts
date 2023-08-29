import { EditorState } from "draft-js";

export const getEditorText = (editorState: EditorState): string =>
  editorState.getCurrentContent().getPlainText();
