"use client";
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
    <div className="relative h-full w-full flex items-start">
      <div className="sticky top-0 max-h-screen overflow-auto">
        <ChatsList />
      </div>
      {children}
    </div>
  );
};

export default Layout;
