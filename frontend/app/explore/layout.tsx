"use client";
import { redirect } from "next/navigation";
import { FC, ReactNode } from "react";
import { useSupabase } from "../supabase-provider";

interface LayoutProps {
  children?: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  const { session } = useSupabase();
  if (!session) {
    redirect("/login");
  }
  return <>{children}</>;
};

export default Layout;
