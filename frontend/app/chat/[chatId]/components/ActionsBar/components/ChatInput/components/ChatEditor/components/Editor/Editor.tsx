import { EditorContent } from "@tiptap/react";
import "./styles.css";

import { useChatStateUpdater } from "./hooks/useChatStateUpdater";
import { useCreateEditorState } from "./hooks/useCreateEditorState";
import { useEditor } from "./hooks/useEditor";
import { useEditorStateUpdater } from "./hooks/useEditorStateUpdater";

type EditorProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
};

export const Editor = ({
  setMessage,
  message,
  onSubmit,
}: EditorProps): JSX.Element => {
  const { editor } = useCreateEditorState();

  useChatStateUpdater({
    editor,
    setMessage,
  });

  useEditorStateUpdater({
    editor,
    message,
  });

  const { submitOnEnter } = useEditor({
    onSubmit,
  });

  return (
    <EditorContent
      className="w-full"
      onKeyDown={submitOnEnter}
      editor={editor}
    />
  );
};
