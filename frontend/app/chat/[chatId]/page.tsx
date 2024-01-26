"use client";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useDevice } from "@/lib/hooks/useDevice";
import { useCustomDropzone } from "@/lib/hooks/useDropzone";
import { cn } from "@/lib/utils";

import { ActionsBar } from "./components/ActionsBar";
import { ChatDialogueArea } from "./components/ChatDialogueArea/ChatDialogue";
import DataPanel from "./components/DataPanel/DataPanel";
import { useChatNotificationsSync } from "./hooks/useChatNotificationsSync";
import styles from "./page.module.scss";

const SelectedChatPage = (): JSX.Element => {
  const { getRootProps } = useCustomDropzone();
  const { shouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { isMobile } = useDevice();

  useChatNotificationsSync();

  return (
    <div
      className={`
      ${styles.chat_page_container ?? ""} 
      ${shouldDisplayFeedCard ? styles.feeding ?? "" : ""}
      `}
      data-testid="chat-page"
      {...getRootProps()}
    >
      <div
        className={cn(
          "flex flex-col flex-1 items-center justify-stretch w-full h-full overflow-hidden",
          "dark:bg-black transition-colors ease-out duration-500"
        )}
      >
        <div
          className={`flex flex-col flex-1 w-full max-w-4xl h-full dark:shadow-primary/25 overflow-hidden`}
        >
          <div className="flex flex-1 flex-col overflow-y-auto">
            <ChatDialogueArea />
          </div>
          <ActionsBar />
        </div>
      </div>
      {!isMobile && (
        <div className={styles.data_panel_wrapper}>
          <DataPanel />
        </div>
      )}
    </div>
  );
};

export default SelectedChatPage;
