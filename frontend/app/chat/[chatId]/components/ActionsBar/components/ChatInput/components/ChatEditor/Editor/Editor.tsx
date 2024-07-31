import { EditorContent } from "@tiptap/react";
import { useEffect } from "react";
import "./styles.css";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

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
  const { currentBrain } = useBrainContext();

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

  useEffect(() => {
    editor?.commands.focus();
  }, [currentBrain, editor]);

  useEffect(() => {
    if (editor && placeholder) {
      (
        editor.extensionManager.extensions.find(
          (ext) => ext.name === "placeholder"
        ) as { options: { placeholder: string } }
      ).options.placeholder = placeholder;
      editor.view.updateState(editor.state);
    }
  }, [placeholder, editor]);

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
      onKeyDown={(event) => {
        if (event.key === "Enter" && !event.shiftKey && !currentBrain) {
          event.preventDefault();
          const lastChar = editor?.state.doc.textBetween(
            editor.state.selection.$from.pos - 1,
            editor.state.selection.$from.pos,
            undefined,
            "\ufffc"
          );
          if (lastChar === " ") {
            editor?.chain().insertContent("@").focus().run();
          } else {
            editor?.chain().insertContent(" @").focus().run();
          }
        } else {
          submitOnEnter(event);
        }
      }}
      editor={editor}
    />
  );
};
