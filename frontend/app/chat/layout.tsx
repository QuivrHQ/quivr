"use client";
import { FC, ReactNode } from "react";
import { ChatsList } from "./components";

interface LayoutProps {
  children?: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen pt-20 overflow-hidden">
      <ChatsList />
      {children}
    </div>
  );
};

export default Layout;
