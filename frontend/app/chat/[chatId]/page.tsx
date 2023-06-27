/* eslint-disable */
"use client";

import Selector from "@/lib/components/ui/Selector";

import { ChatInput, ChatMessages } from "../components";
import { ChatProvider } from "./context/ChatContext";

export default function ChatPage() {
  return (
    <main className="flex flex-col w-full pt-10">
      <section className="flex flex-col flex-1 items-center w-full h-full min-h-screen">
        
        <ChatProvider>
          <div className="my-4">
            <Selector choice1="Ask Brain" choice2="Just Chat" />
          </div>
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
}
