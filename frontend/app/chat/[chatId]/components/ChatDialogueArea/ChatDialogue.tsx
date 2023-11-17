import { useParams } from "next/navigation";

import { useChatContext } from "@/lib/context";
import { useSecurity } from "@/services/useSecurity/useSecurity";

// eslint-disable-next-line import/order
import { ChatGuide } from "../ChatGuide";
import { ChatDialogue } from "./components/ChatDialogue";
import { ShortCuts } from "./components/ShortCuts";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "./utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";

export const ChatDialogueArea = (): JSX.Element => {
  const { isStudioMember } = useSecurity();
  const params = useParams();

  const { messages, notifications, isLoadingHistoryChatItems } =
    useChatContext();

  const chatItems = getMergedChatMessagesWithDoneStatusNotificationsReduced(
    messages,
    notifications
  );

  // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
  const shouldDisplayShortcuts = !isLoadingHistoryChatItems && !params?.chatId;

  if (!shouldDisplayShortcuts) {
    return (
      <div className="flex flex-col flex-1 overflow-y-auto mb-2">
        <ChatDialogue chatItems={chatItems} />
      </div>
    );
  }

  return isStudioMember ? <ShortCuts /> : <ChatGuide />;
};
