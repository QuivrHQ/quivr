import { useParams } from "next/navigation";

import { useChatContext } from "@/lib/context";

// eslint-disable-next-line import/order
import { ChatGuide } from "../ChatGuide";
import { ChatDialogue } from "./components/ChatDialogue";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "./utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";

export const ChatDialogueArea = (): JSX.Element => {
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

  return <ChatGuide />;
};
