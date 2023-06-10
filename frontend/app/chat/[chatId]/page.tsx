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
    <main className="flex flex-col w-full">
      <section className="flex flex-col items-center w-full overflow-auto">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        {chat && <ChatMessages chat={chat} />}
        <ChatInput chatId={chatId} {...others} />
      </section>
    </main>
  );
}
