"use client";
import { ChatsProvider } from "@/lib/context/ChatsProvider/chats-provider";
import { redirect } from "next/navigation";
import { FC, ReactNode } from "react";
import { useSupabase } from "../supabase-provider";
import { ChatsList } from "./components";

interface LayoutProps {
  children?: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  const { session } = useSupabase();
  if (!session) redirect("/login");

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
