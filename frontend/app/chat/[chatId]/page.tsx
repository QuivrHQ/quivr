"use client";

import { UUID } from "crypto";
import { useEffect } from "react";

import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { useChatContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useDevice } from "@/lib/hooks/useDevice";
import { useCustomDropzone } from "@/lib/hooks/useDropzone";
import { ButtonType } from "@/lib/types/QuivrButton";
import { cn } from "@/lib/utils";

import { ActionsBar } from "./components/ActionsBar";
import { ChatDialogueArea } from "./components/ChatDialogueArea/ChatDialogue";
import DataPanel from "./components/DataPanel/DataPanel";
import { useChatNotificationsSync } from "./hooks/useChatNotificationsSync";
import styles from "./page.module.scss";

const SelectedChatPage = (): JSX.Element => {
  const { getRootProps } = useCustomDropzone();
  const { isMobile } = useDevice();

  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { setIsBrainCreationModalOpened } = useBrainCreationContext();

  const { currentBrain, setCurrentBrainId } = useBrainContext();
  const { messages } = useChatContext();

  useChatNotificationsSync();

  const buttons: ButtonType[] = [
    {
      label: "Create brain",
      color: "primary",
      onClick: () => {
        setIsBrainCreationModalOpened(true);
      },
      iconName: "brain",
    },
    {
      label: "Add knowledge",
      color: "primary",
      onClick: () => {
        setShouldDisplayFeedCard(true);
      },
      iconName: "uploadFile",
      hidden: !currentBrain?.max_files,
    },
    {
      label: "Manage current brain",
      color: "primary",
      onClick: () => {
        window.location.href = `/studio/${currentBrain?.id}`;
      },
      iconName: "edit",
    },
  ];

  useEffect(() => {
    if (!currentBrain && messages.length > 0) {
      setCurrentBrainId(messages[messages.length - 1].brain_id as UUID);
    }
  }, [messages]);

  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="chat" label="Chat" buttons={buttons} />
      </div>
      <div
        className={styles.chat_page_container}
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
        <UploadDocumentModal />
        <AddBrainModal />
      </div>
    </div>
  );
};

export default SelectedChatPage;
