"use client";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

import { ChatsProvider } from "@/lib/context/ChatsProvider/chats-provider";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import { ChatsList } from "./components";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  const { session } = useSupabase();
  if (session === null) {
    redirect("/login");
  }

  return (
    <ChatsProvider>
      <div className="relative h-full w-full flex items-start">
        <ChatsList />
        {children}
      </div>
    </ChatsProvider>
  );
};

export default Layout;
