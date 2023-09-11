import { useChatContext } from "@/lib/context";

import { MessagesDialog } from "./MessagesDialog";
import { ShortCuts } from "./ShortCuts";

export const ChatDialog = (): JSX.Element => {
  const { messages } = useChatContext();

  const shouldDisplayShortcuts = messages.length === 0;

  if (!shouldDisplayShortcuts) {
    return <MessagesDialog />;
  }

  return <ShortCuts />;
};
