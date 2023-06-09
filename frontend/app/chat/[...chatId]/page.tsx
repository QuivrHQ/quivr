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
    <main className="w-4/5 flex flex-col overflow-auto">
      <section className="flex flex-col justify-center items-center flex-1 overflow-auto">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        <Card className="p-5 max-w-3xl w-full flex-1 mb-24 overflow-auto flex flex-col ">
          <ChatMessages history={chat?.history ?? []} />
        </Card>
        <Card className="fixed  w-full max-w-3xl bg-gray-100 dark:bg-gray-800 rounded-b-none  bottom-16 px-5 py-5">
          <ChatInput chatId={chatId} />
        </Card>
      </section>
    </main>
  );
}
