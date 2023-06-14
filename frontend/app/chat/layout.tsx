"use client";
import { redirect } from "next/navigation";
import { FC, ReactNode } from "react";

import { ChatsProvider } from "@/lib/context/ChatsProvider/chats-provider";

import { ChatsList } from "./components";
import { useSupabase } from "../supabase-provider";

interface LayoutProps {
  children?: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  const { session } = useSupabase();
  if (!session) {redirect("/login");}

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
