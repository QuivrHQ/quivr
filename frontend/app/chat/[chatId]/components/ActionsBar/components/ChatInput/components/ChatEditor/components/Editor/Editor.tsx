import { EditorContent } from "@tiptap/react";
import "./styles.css";

import { useChatStateUpdater } from "./hooks/useChatStateUpdater";
import { useCreateEditorState } from "./hooks/useCreateEditorState";
import { useEditor } from "./hooks/useEditor";

type EditorProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
};

export const Editor = ({ setMessage, onSubmit }: EditorProps): JSX.Element => {
  const { editor } = useCreateEditorState();

  useChatStateUpdater({
    editor,
    setMessage,
  });

  const { submitOnEnter } = useEditor({
    onSubmit,
  });

  return (
    <EditorContent
      className="w-full"
      onKeyDown={(event) => void submitOnEnter(event)}
      editor={editor}
    />
  );
};
