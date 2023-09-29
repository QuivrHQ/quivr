"use client";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useCustomDropzone } from "@/lib/hooks/useDropzone";

import { ActionsBar } from "./components/ActionsBar";
import { ChatDialogueArea } from "./components/ChatDialogueArea/ChatDialogue";
import { ChatHeader } from "./components/ChatHeader";

const SelectedChatPage = (): JSX.Element => {
  const { getRootProps } = useCustomDropzone();
  const { shouldDisplayFeedCard } = useKnowledgeToFeedContext();

  return (
    <main
      className="flex flex-col w-full h-[calc(100vh-61px)] overflow-hidden"
      data-testid="chat-page"
      {...getRootProps()}
    >
      <section className="flex flex-col flex-1 items-center w-full h-full overflow-y-auto">
        <ChatHeader />
        <div
          className={`flex-1 flex flex-col mt-4 md:mt-8 w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden dark:bg-black border border-black/10 dark:border-white/25 p-2 md:p-12 pt-4 md:pt-10   ${
            shouldDisplayFeedCard ? "bg-chat-bg-gray" : "bg-white"
          }`}
        >
          <div className="flex flex-1 flex-col overflow-y-auto">
            <ChatDialogueArea />
          </div>
          <ActionsBar />
        </div>
      </section>
    </main>
  );
};

export default SelectedChatPage;
