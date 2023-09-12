import { useChatContext } from "@/lib/context";

import { MessagesDialogue } from "./components/MessagesDialog";
import { ShortCuts } from "./components/ShortCuts";
import { getMergedChatMessagesWithReducedNotifications } from "./utils/getMergedChatMessagesWithReducedNotifications";

export const ChatDialogue = (): JSX.Element => {
  const { messages, notifications } = useChatContext();

  const chatItems = getMergedChatMessagesWithReducedNotifications(
    messages,
    notifications
  );
  const notificationsWithStatusDone = notifications.map(
    (notification) => notification.status === "Done"
  );

  const shouldDisplayShortcuts =
    messages.length === 0 && notificationsWithStatusDone.length === 0;

  if (!shouldDisplayShortcuts) {
    return <MessagesDialogue chatItems={chatItems} />;
  }

  return <ShortCuts />;
};
