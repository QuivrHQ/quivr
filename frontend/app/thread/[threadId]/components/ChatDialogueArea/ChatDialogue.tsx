import { useThreadContext } from "@/lib/context";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { ThreadDialogue } from "./components/ThreadDialogue";
import { getMergedThreadMessagesWithDoneStatusNotificationsReduced } from "./utils/getMergedThreadMessagesWithDoneStatusNotificationsReduced";

export const ThreadDialogueArea = (): JSX.Element => {
  const { messages, notifications } = useThreadContext();

  const chatItems = getMergedThreadMessagesWithDoneStatusNotificationsReduced(
    messages,
    notifications
  );
  const { isOnboarding } = useOnboarding();

  const shouldDisplayShortcuts = chatItems.length === 0 && !isOnboarding;

  if (!shouldDisplayShortcuts) {
    return <ThreadDialogue chatItems={chatItems} />;
  }

  return <></>;
};
