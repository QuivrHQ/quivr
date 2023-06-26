/* eslint-disable */
"use client";

import PageHeading from "@/lib/components/ui/PageHeading";

import { ChatInput, ChatMessages } from "../components";
import { ChatProvider } from "./context/ChatContext";

export default function ChatPage() {
  return (
    <main className="flex flex-col w-full pt-10">
      <section className="flex flex-col flex-1 items-center w-full h-full min-h-screen">
        <PageHeading
                  title="专有知识库聊天机器人(vantoo)"
                  subtitle="输入基于知识库内容的相关问题，通过gpt的大语言模型能力，可以总结文档内容， 快速查找知识点，进行相关性查询等，为你提供最佳答案"
        />
        <ChatProvider>
          <div className="relative h-full w-full flex flex-col flex-1 items-center">
            <div className="h-full flex-1 w-full flex flex-col items-center">
              <ChatMessages />
            </div>
            <ChatInput />
          </div>
        </ChatProvider>
      </section>
    </main>
  );
}
