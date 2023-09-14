"use client";

import { ActionsBar } from "./components/ActionsBar";
import { ChatDialogueArea } from "./components/ChatDialogueArea/ChatDialogue";
import { ChatHeader } from "./components/ChatHeader";

const SelectedChatPage = (): JSX.Element => {
  return (
    <main className="flex flex-col w-full h-[calc(100vh-61px)] overflow-hidden" data-testid="chat-page">
    <section className="flex flex-col flex-1 items-center w-full h-full overflow-y-auto">
        <ChatHeader /> {/* Added margin-bottom */}
        <div className="flex-1 flex flex-col mt-4 md:mt-8 w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2 md:p-12 pt-4 md:pt-10">
            <div className="flex flex-1 flex-col overflow-y-auto">
                <ChatDialogueArea />
            </div>
            <ActionsBar/> {/* Added margin-top */}
        </div>
    </section>
  </main>
  );
};

export default SelectedChatPage;
