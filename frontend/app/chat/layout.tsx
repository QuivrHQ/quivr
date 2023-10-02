"use client";
import { ReactNode } from "react";

import { ChatProvider, KnowledgeToFeedProvider } from "@/lib/context";
import { ChatsProvider } from "@/lib/context/ChatsProvider/chats-provider";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { ChatsList } from "./components/ChatsList";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  const { session } = useSupabase();

  if (session === null) {
    redirectToLogin();
  }

  return (
    <KnowledgeToFeedProvider>
      <ChatsProvider>
        <ChatProvider>
          <div className="relative h-full w-full flex justify-stretch items-stretch">
            <ChatsList />
            {children}
          </div>
        </ChatProvider>
      </ChatsProvider>
    </KnowledgeToFeedProvider>
  );
};

export default Layout;
