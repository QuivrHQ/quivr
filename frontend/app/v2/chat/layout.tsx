"use client";
import { ReactNode } from "react";

import { ChatsList } from "@/app/chat/components";
import { ChatsProvider } from "@/lib/context/ChatsProvider/chats-provider";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  const { session } = useSupabase();
  if (session === null) {
    redirectToLogin();
  }

  return (
    <ChatsProvider>
      <div className="relative h-full w-full flex justify-stretch items-stretch">
        <ChatsList />
        {children}
      </div>
    </ChatsProvider>
  );
};

export default Layout;
