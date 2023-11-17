"use client";

import { ChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/components/ChatItem";
import {
  chatDialogueContainerClassName,
  chatItemContainerClassName,
} from "@/app/chat/[chatId]/components/ChatDialogueArea//components/ChatDialogue/styles";
import { getKeyFromChatItem } from "@/app/chat/[chatId]/components/ChatDialogueArea/components/ChatDialogue/utils/getKeyFromChatItem";
import { useSharedChatItems } from "@/app/shared/components/hooks/useSharedChatItems";
import Spinner from "@/lib/components/ui/Spinner";
import { useChatContext } from "@/lib/context";

export const DisplayChatMessageArea = (): JSX.Element => {
  const { sharedChatItems } = useChatContext();
  const { isLoading } = useSharedChatItems();

  return (
    <div className={chatDialogueContainerClassName}>
      {isLoading && (
        <div className="h-full flex justify-center items-center">
          <Spinner />
        </div>
      )}
      {!isLoading && sharedChatItems.length > 0 && (
        <div>
          <div className={chatItemContainerClassName}>
            {sharedChatItems.map((chatItem) => (
              <ChatItem key={getKeyFromChatItem(chatItem)} content={chatItem} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
