import { Disclaimer } from "@/lib/components/Disclaimer";
import { useChatContext } from "@/lib/context";
import { useOnboarding } from "@/lib/hooks/useOnboarding";
import { useSecurity } from "@/services/useSecurity/useSecurity";

import { ChatDialogue } from "./components/ChatDialogue";
import { ShortCuts } from "./components/ShortCuts";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "./utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";

export const ChatDialogueArea = (): JSX.Element => {
  const { isStudioMember } = useSecurity();

  const { messages, notifications } = useChatContext();

  const chatItems = getMergedChatMessagesWithDoneStatusNotificationsReduced(
    messages,
    notifications
  );
  const { isOnboarding } = useOnboarding();

  const shouldDisplayShortcuts = chatItems.length === 0 && !isOnboarding;

  if (!shouldDisplayShortcuts) {
    return (
      <div className="flex flex-col flex-1 overflow-y-auto mb-2">
        <div>
          <Disclaimer />
        </div>
        <ChatDialogue chatItems={chatItems} />
      </div>
    );
  }

  return isStudioMember ? <ShortCuts /> : <></>;
};
