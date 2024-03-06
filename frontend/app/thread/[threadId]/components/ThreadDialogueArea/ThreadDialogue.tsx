import { useThreadContext } from "@/lib/context";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { ThreadDialogue } from "./components/ThreadDialogue";
import { getMergedThreadMessagesWithDoneStatusNotificationsReduced } from "./utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";

export const ThreadDialogueArea = (): JSX.Element => {
  const { messages, notifications } = useThreadContext();

  const threadItems = getMergedThreadMessagesWithDoneStatusNotificationsReduced(
    messages,
    notifications
  );
  const { isOnboarding } = useOnboarding();

  const shouldDisplayShortcuts = threadItems.length === 0 && !isOnboarding;

  if (!shouldDisplayShortcuts) {
    return <ThreadDialogue threadItems={threadItems} />;
  }

  return <></>;
};
