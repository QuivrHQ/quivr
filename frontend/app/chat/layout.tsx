"use client";
import { useRouter } from "next/navigation";
import { FC, ReactNode, useState } from "react";
import { ChatsList } from "./components";
import { Chat } from "./types";

interface LayoutProps {
  children?: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  const [chats, setChats] = useState<Chat[]>([]);
  const router = useRouter();

  return (
    <div className="flex h-screen pt-20 overflow-hidden">
      <aside className="w-1/5 h-full border-r overflow-auto">
        <ChatsList chats={chats} setChats={setChats} router={router} />
      </aside>
      {children}
    </div>
  );
};

export default Layout;
