import { Editor } from "@tiptap/core";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useChatStateUpdater } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/Editor/hooks/useChatStateUpdater";
import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { ChatBar } from "@/lib/components/ui/ChatBar/ChatBar";

export const TextEditorSearchBar = ({
  onSearch,
  newBrain,
  editor,
}: {
  onSearch?: () => void;
  newBrain?: boolean;
  editor: Editor;
}): JSX.Element => {
  const chatInput = useChatInput();
  const { messages } = useChat();
  const router = useRouter();

  useChatStateUpdater({ editor, setMessage: chatInput.setMessage });

  useEffect(() => {
    if (chatInput.generatingAnswer || messages.length <= 0) {
      return;
    }
    editor.commands.insertContent(messages[0].assistant);
  }, [messages.length, router, editor, chatInput.generatingAnswer]);

  return (
    <ChatBar
      onSearch={() => {
        if (!chatInput.chatId && messages.length > 0) {
          router.replace(`/note/${messages[0].chat_id}`);
        }
        onSearch?.();
      }}
      newBrain={newBrain}
      {...chatInput}
    />
  );
};
