import { useChatContext } from "@/lib/context";

import { MessagesDialog } from "./MessagesDialog";
import { ShortCuts } from "./ShortCuts";

export const ChatDialog = (): JSX.Element => {
  const { messages, notifications } = useChatContext();

  const shouldDisplayShortcuts =
    messages.length === 0 && notifications.length === 0;

  if (!shouldDisplayShortcuts) {
    return <MessagesDialog />;
  }

  return <ShortCuts />;
};
