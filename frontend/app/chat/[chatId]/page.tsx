"use client";

import { useMenuWidth } from "@/lib/components/Menu/hooks/useMenuWidth";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useCustomDropzone } from "@/lib/hooks/useDropzone";
import { cn } from "@/lib/utils";

import { ActionsBar } from "./components/ActionsBar";
import { ChatDialogueArea } from "./components/ChatDialogueArea/ChatDialogue";
import { useChatNotificationsSync } from "./hooks/useChatNotificationsSync";
import { useChatsList } from "./hooks/useChatsList";

const SelectedChatPage = (): JSX.Element => {
  const { getRootProps } = useCustomDropzone();
  const { shouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { shouldDisplayRightSideBar, OPENED_MENU_WIDTH } = useMenuWidth();

  useChatsList();
  useChatNotificationsSync();

  return (
    <div className="flex flex-1">
      <div
        className={cn(
          "flex flex-col flex-1 items-center justify-stretch w-full h-full overflow-hidden",
          shouldDisplayFeedCard ? "bg-chat-bg-gray" : "bg-tertiary",
          "dark:bg-black transition-colors ease-out duration-500"
        )}
        data-testid="chat-page"
        {...getRootProps()}
      >
        <div
          className={`flex flex-col flex-1 w-full max-w-5xl h-full dark:shadow-primary/25 overflow-hidden p-2 sm:p-4 md:p-6 lg:p-8`}
        >
          <div className="flex flex-1 flex-col overflow-y-auto">
            <ChatDialogueArea />
          </div>
          <ActionsBar />
        </div>
      </div>
      {shouldDisplayRightSideBar && (
        <div
          className="h-full bg-highlight"
          style={{ width: OPENED_MENU_WIDTH }}
        />
      )}
    </div>
  );
};

export default SelectedChatPage;
