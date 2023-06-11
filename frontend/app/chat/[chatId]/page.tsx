"use client";
import { UUID } from "crypto";
import PageHeading from "../../components/ui/PageHeading";
import { ChatInput, ChatMessages } from "../components";
import useChats from "../hooks/useChats";

interface ChatPageProps {
  params?: {
    chatId?: UUID;
  };
}

export default function ChatPage({ params }: ChatPageProps) {
  const chatId: UUID | undefined = params?.chatId;

  const { chat, ...others } = useChats(chatId);

  return (
    <main className="flex flex-col w-full pt-10">
      <section className="flex flex-col flex-1 items-center w-full h-full min-h-screen">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        <div className="relative h-full w-full flex flex-col flex-1 items-center">
          <div className="h-full flex-1 w-full flex flex-col items-center">
            {chat && <ChatMessages chat={chat} />}
          </div>
          <ChatInput chatId={chatId} {...others} />
        </div>
      </section>
    </main>
  );
}
