import { useFeatureIsOn } from "@growthbook/growthbook-react";

import { useChatContext } from "@/lib/context";

import { ChatDialogue } from "./components/ChatDialogue";
import { ShortCuts } from "./components/ShortCuts";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "./utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";

export const ChatDialogueArea = (): JSX.Element => {
  const { messages, notifications } = useChatContext();

  const chatItems = getMergedChatMessagesWithDoneStatusNotificationsReduced(
    messages,
    notifications
  );
  const shouldDisplayOnboarding = useFeatureIsOn("onboarding");

  const shouldDisplayShortcuts =
    chatItems.length === 0 && !shouldDisplayOnboarding;

  if (!shouldDisplayShortcuts) {
    return <ChatDialogue chatItems={chatItems} />;
  }

  return <ShortCuts />;
};
