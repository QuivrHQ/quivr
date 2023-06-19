/* eslint-disable */
"use client";
import { UUID } from "crypto";
import { useEffect } from "react";

import PageHeading from "@/lib/components/ui/PageHeading";
import useChatsContext from "@/lib/context/ChatsProvider/hooks/useChatsContext";

import { ChatInput, ChatMessages } from "../components";

interface ChatPageProps {
  params: {
    chatId: UUID;
  };
}

export default function ChatPage({ params }: ChatPageProps) {
  const chatId: UUID | undefined = params.chatId;

  const { fetchChat, resetChat } = useChatsContext();

  useEffect(() => {
    // if (chatId)
    if (!chatId) {
      resetChat();
    }
    fetchChat(chatId);
  }, [fetchChat, chatId]);

  return (
    <main className="flex flex-col w-full pt-10">
      <section className="flex flex-col flex-1 items-center w-full h-full min-h-screen">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        <div className="relative h-full w-full flex flex-col flex-1 items-center">
          <div className="h-full flex-1 w-full flex flex-col items-center">
            <ChatMessages />
          </div>
          <ChatInput />
        </div>
      </section>
    </main>
  );
}
