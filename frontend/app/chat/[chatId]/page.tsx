"use client";

import { ChatProvider } from "@/lib/context/ChatProvider";

import { ChatInput, ChatMessages } from "./components";
import { ChatHeader } from "./components/ChatHeader";

const SelectedChatPage = (): JSX.Element => {
  return (
    <ChatProvider>
      <main className="flex flex-col w-full pt-10" data-testid="chat-page">
        <section className="flex flex-col flex-1 items-center w-full h-full min-h-[70vh]">
          <ChatHeader />
          <div className="relative w-full flex flex-col flex-1 items-center">
            <div className="flex-1 w-full flex flex-col items-center">
              <ChatMessages />
            </div>
            <ChatInput />
          </div>
        </section>
      </main>
    </ChatProvider>
  );
};

export default SelectedChatPage;
