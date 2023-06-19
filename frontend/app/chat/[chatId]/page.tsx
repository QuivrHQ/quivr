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
                  title="专有知识库聊天机器人(vantoo)"
                  subtitle="输入基于知识库内容的相关问题，通过gpt的大语言模型能力，可以总结文档内容， 快速查找知识点，进行相关性查询等，为你提供最佳答案"
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
