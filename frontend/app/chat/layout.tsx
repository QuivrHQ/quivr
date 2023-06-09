"use client";
import { useRouter } from "next/navigation";
import { FC, ReactNode, useState } from "react";
import { ChatsList } from "./components";
import { Chat } from "./types";

interface LayoutProps {
  children?: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen pt-20 overflow-hidden">
      <aside className="w-1/5 h-full border-r overflow-auto">
        <ChatsList />
      </aside>
      {children}
    </div>
  );
};

export default Layout;
