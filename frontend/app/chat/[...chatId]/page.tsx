"use client";
import { UUID } from "crypto";
import Card from "../../components/ui/Card";
import PageHeading from "../../components/ui/PageHeading";
import { ChatInput, ChatMessages } from "../components";
import useChats from "../hooks/useChats";

interface ChatPageProps {
  params?: {
    chatId?: UUID;
  };
}

export default function ChatPage({ params }: ChatPageProps) {
  let chatId: UUID | undefined;
  chatId = params?.chatId;

  const { chat } = useChats(chatId);

  return (
    <main className="flex flex-col overflow-auto w-full">
      <section className="flex flex-col items-center w-full flex-1 overflow-auto">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        <Card className="p-5 max-w-5xl w-full flex-1 mb-24 overflow-auto flex flex-col ">
          <ChatMessages history={chat?.history ?? []} />
        </Card>
        <ChatInput chatId={chatId} />
      </section>
    </main>
  );
}
