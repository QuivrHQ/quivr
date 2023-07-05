"use client";

import PageHeading from "@/lib/components/ui/PageHeading";
import { ChatProvider } from "@/lib/context/ChatProvider";

import { ChatInput, ChatMessages } from "./components";

const SelectedChatPage = (): JSX.Element => {
  return (
    <main className="flex flex-col w-full pt-10" data-testid="chat-page">
      <section className="flex flex-col flex-1 items-center w-full h-full min-h-[70vh]">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        <ChatProvider>
          <div className="relative w-full flex flex-col flex-1 items-center">
            <div className="flex-1 w-full flex flex-col items-center">
              <ChatMessages />
            </div>
            <ChatInput />
          </div>
        </ChatProvider>
      </section>
    </main>
  );
};

export default SelectedChatPage;
