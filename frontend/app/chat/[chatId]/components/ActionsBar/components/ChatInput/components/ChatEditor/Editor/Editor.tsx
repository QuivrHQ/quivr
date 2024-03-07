import { EditorContent } from "@tiptap/react";
import { useEffect } from "react";
import "./styles.css";

import { useChatStateUpdater } from "./hooks/useChatStateUpdater";
import { useCreateEditorState } from "./hooks/useCreateEditorState";
import { useEditor } from "./hooks/useEditor";

type EditorProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
  placeholder?: string;
};

export const Editor = ({
  setMessage,
  onSubmit,
  placeholder,
  message,
}: EditorProps): JSX.Element => {
  const { editor } = useCreateEditorState(placeholder);

  useEffect(() => {
    const htmlString = editor?.getHTML();
    if (
      message === "" ||
      (htmlString &&
        new DOMParser().parseFromString(htmlString, "text/html").body
          .textContent === " ")
    ) {
      editor?.commands.clearContent();
    }
  }, [message, editor]);

  useChatStateUpdater({
    editor,
    setMessage,
  });

  const { submitOnEnter } = useEditor({
    onSubmit,
  });

  return (
    <EditorContent
      className="w-full caret-accent"
      onKeyDown={(event) => void submitOnEnter(event)}
      editor={editor}
    />
  );
};
