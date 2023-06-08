"use client";
import { useAxios } from "@/lib/useAxios";
import { UUID } from "crypto";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Card from "../../components/ui/Card";
import PageHeading from "../../components/ui/PageHeading";
import { ChatInput, ChatMessages, ChatsList } from "../components";
import { useQuestion } from "../hooks/useQuestion";
import { Chat } from "../types";

interface ChatPageProps {
  params: {
    chatId?: UUID;
  };
}

export default function ChatPage({ params }: ChatPageProps) {
  const { chatId } = params;
  const [chats, setChats] = useState<Chat[]>([]);
  const router = useRouter();

  const question = useQuestion({
    chatId: chatId,
    setChats,
  });
  const { axiosInstance } = useAxios();

  const { setHistory } = question;
  useEffect(() => {
    const fetchChatHistory = async () => {
      if (!chatId) return; // Skip fetching history if chatId is not present (i.e., a new chat)

      try {
        console.log(
          `Fetching history from ${process.env.NEXT_PUBLIC_BACKEND_URL}/chat/${chatId}`
        );
        const response = await axiosInstance.get<{
          history: Array<[string, string]>;
        }>(`/chat/${chatId}`);
        setHistory(response.data.history);
      } catch (error) {
        console.error("Error fetching the history of this chat", error);
        setHistory([]);
      }
    };

    fetchChatHistory();
  }, [chatId, setHistory, axiosInstance]);

  return (
    <div className="flex h-screen pt-20 overflow-hidden">
      <aside className="w-1/5 h-full border-r overflow-auto">
        <ChatsList chats={chats} setChats={setChats} router={router} />
      </aside>
      <main className="w-4/5 flex flex-col overflow-auto">
        <section className="flex flex-col justify-center items-center flex-1 overflow-auto">
          <PageHeading
            title="Chat with your brain"
            subtitle="Talk to a language model about your uploaded data"
          />
          <Card className="p-5 max-w-3xl w-full flex-1 mb-24 overflow-auto flex flex-col ">
            <ChatMessages history={question.history} />
          </Card>
          <Card className="fixed  w-full max-w-3xl bg-gray-100 dark:bg-gray-800 rounded-b-none  bottom-16 px-5 py-5">
            <ChatInput {...question} />
          </Card>
        </section>
      </main>
    </div>
  );
}
