"use client";
import { ReactNode } from "react";

import { ChatProvider, KnowledgeToFeedProvider } from "@/lib/context";
import { ChatsProvider } from "@/lib/context/ChatsProvider/chats-provider";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  return (
    <KnowledgeToFeedProvider>
      <ChatsProvider>
        <ChatProvider>
          <div className="relative h-full w-full flex justify-stretch items-stretch">
            {children}
          </div>
        </ChatProvider>
      </ChatsProvider>
    </KnowledgeToFeedProvider>
  );
};

export default Layout;
