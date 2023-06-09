"use client";
import { UUID } from "crypto";
import { useEffect } from "react";
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

  const {
    chat,
    fetchChat,
    sendMessage,
    isSendingMessage,
    message,
    setMessage,
  } = useChats();

  useEffect(() => {
    if (!chatId) return;
    fetchChat(chatId);
    //   const fetchChatHistory = async () => {
    //     if (!chatId) return; // Skip fetching history if chatId is not present (i.e., a new chat)

    //     try {
    //       console.log(
    //         `Fetching history from ${process.env.NEXT_PUBLIC_BACKEND_URL}/chat/${chatId}`
    //       );
    //       const response = await axiosInstance.get<{
    //         history: ChatHistory;
    //       }>(`/chat/${chatId}`);
    //       questionParams.setHistory(response.data.history);
    //     } catch (error) {
    //       console.error("Error fetching the history of this chat", error);
    //       questionParams.setHistory([]);
    //     }
    //   };

    //   fetchChatHistory();
  }, []);

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
          <ChatInput
            askQuestion={() => sendMessage(chatId)}
            history={chat?.history ?? []}
            isPending={isSendingMessage}
            question={message[1]}
            setQuestion={(value) => {
              setMessage((msg) => [msg[0], value.toString()]);
              return value;
            }}
          />
        </Card>
      </section>
    </main>
  );
}
