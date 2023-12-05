"use client";

import { useRef } from "react";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useCustomDropzone } from "@/lib/hooks/useDropzone";

import { ActionsBar } from "./components/ActionsBar";
import { ChatDialogueArea } from "./components/ChatDialogueArea/ChatDialogue";

const SelectedChatPage = (): JSX.Element => {
  const { getRootProps } = useCustomDropzone();
  const { shouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const ChatDialogueAreaRef = useRef(null);

  return (
    <div
      className={`flex flex-col flex-1 items-center justify-stretch w-full h-full overflow-hidden ${
        shouldDisplayFeedCard ? "bg-chat-bg-gray" : "bg-white"
      } dark:bg-black transition-colors ease-out duration-500`}
      data-testid="chat-page"
      {...getRootProps()}
    >
      <div
        className={`flex flex-col flex-1 w-full max-w-5xl h-full dark:shadow-primary/25 overflow-hidden px-2 pb-2 pt-10 sm:px-4 sm:pt-12 md:px-6 lg:px-10 relative`}
      >
        <div
          className="flex flex-1 flex-col overflow-y-auto"
          ref={ChatDialogueAreaRef}
        >
          <ChatDialogueArea />
        </div>
        <ActionsBar />
      </div>
    </div>
  );
};

export default SelectedChatPage;
