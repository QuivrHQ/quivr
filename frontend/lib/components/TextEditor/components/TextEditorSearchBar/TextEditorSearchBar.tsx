import { Editor } from "@tiptap/core";
import { useRouter } from "next/navigation";
import { forwardRef, useEffect } from "react";

import { useChatStateUpdater } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/Editor/hooks/useChatStateUpdater";
import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { ChatBar } from "@/lib/components/ui/ChatBar/ChatBar";

import { useAiContext } from "../../hooks/useAiContext";

type TextEditorSearchBarProps = {
  onSearch?: () => void;
  newBrain?: boolean;
  editor: Editor;
};

const TextEditorSearchBar = forwardRef<Editor, TextEditorSearchBarProps>(
  ({ onSearch, newBrain, editor }, ref): JSX.Element => {
    const { submitQuestion, ...chatInput } = useChatInput();
    const { aiContext, deleteContent } = useAiContext();
    const { messages } = useChat();
    const router = useRouter();

    useChatStateUpdater({ editor, setMessage: chatInput.setMessage });

    useEffect(() => {
      if (chatInput.generatingAnswer || messages.length <= 0) {
        return;
      }

      deleteContent(editor);
      editor.commands.createAiResponse({
        content: messages[0].assistant,
        context: aiContext,
      });
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
        submitQuestion={(question) =>
          submitQuestion(`${aiContext} \n ${question}`, false)
        }
        {...chatInput}
      />
    );
  }
);

TextEditorSearchBar.displayName = "TextEditorSearchBar";

export { TextEditorSearchBar };
