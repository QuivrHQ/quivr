import { Editor } from "@tiptap/core";
import { useRouter } from "next/navigation";
import { forwardRef, useEffect } from "react";

import { useChatStateUpdater } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/Editor/hooks/useChatStateUpdater";
import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { ChatBar } from "@/lib/components/ui/ChatBar/ChatBar";

type TextEditorSearchBarProps = {
  onSearch?: () => void;
  newBrain?: boolean;
  editor: Editor;
};

const TextEditorSearchBar = forwardRef<Editor, TextEditorSearchBarProps>(
  ({ onSearch, newBrain, editor }, ref): JSX.Element => {
    const { submitQuestion, ...chatInput } = useChatInput();
    const { messages } = useChat();
    const router = useRouter();

    useChatStateUpdater({ editor, setMessage: chatInput.setMessage });

    useEffect(() => {
      if (chatInput.generatingAnswer || messages.length <= 0) {
        return;
      }

      editor
        .chain()
        .setAiHighlight()
        .insertContent(messages[0].assistant)
        .focus()
        .run();
    }, [messages.length, router, editor, chatInput.generatingAnswer]);

    useEffect(() => {
      if (chatInput.generatingAnswer) {
        editor.setEditable(false);
      } else {
        editor.setEditable(true);
        editor.commands.focus();
      }
    }, [editor, chatInput.generatingAnswer]);

    return (
      <ChatBar
        ref={ref}
        onSearch={onSearch}
        newBrain={newBrain}
        submitQuestion={(question) => submitQuestion(question, false)}
        {...chatInput}
      />
    );
  }
);

TextEditorSearchBar.displayName = "TextEditorSearchBar";

export { TextEditorSearchBar };
