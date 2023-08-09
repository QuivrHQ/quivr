import { useChatContext } from "@/lib/context";

import { ChatMessages } from "./ChatMessages";
import { ShortCuts } from "./ShortCuts";

export const ChatDialog = (): JSX.Element => {
  const { history } = useChatContext();

  const shouldDisplayShortcuts = history.length === 0;

  if (!shouldDisplayShortcuts) {
    return <ChatMessages />;
  }

  return <ShortCuts />;
};
