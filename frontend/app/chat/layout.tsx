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
    <div className="relative h-full w-full flex pt-20">
      <div className="h-full">
        <ChatsList />
      </div>
      {children}
    </div>
  );
};

export default Layout;
