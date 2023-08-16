"use client";

import { ActionsBar } from "./components/ActionsBar";
import { ChatHeader } from "./components/ChatHeader";
import { ChatDialog } from "./components/Dialog";

const SelectedChatPage = (): JSX.Element => {
  return (
    <main className="flex flex-col w-full pt-10" data-testid="chat-page">
      <section className="flex flex-col flex-1 items-center w-full h-full min-h-[70vh]">
        <ChatHeader />
        <div className="flex-1 flex flex-col mt-8 w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25 p-12 pt-10 max-h-[80vh]">
          <div className="flex flex-1 flex-col overflow-hidden">
            <ChatDialog />
          </div>
          <ActionsBar />
        </div>
      </section>
    </main>
  );
};

export default SelectedChatPage;
