import { useChatContext } from "@/lib/context";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { ChatDialogue } from "./components/ChatDialogue";
import { ShortCuts } from "./components/ShortCuts";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "./utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";

export const ChatDialogueArea = (): JSX.Element => {
  const { messages, notifications } = useChatContext();

  const chatItems = getMergedChatMessagesWithDoneStatusNotificationsReduced(
    messages,
    notifications
  );
  const { isOnboarding } = useOnboarding();

  const shouldDisplayShortcuts = chatItems.length === 0 && !isOnboarding;

  if (!shouldDisplayShortcuts) {
    return <ChatDialogue chatItems={chatItems} />;
  }

  return <ShortCuts />;
};
