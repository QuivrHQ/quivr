"use client";
import { ReactNode } from "react";

import { KnowledgeProvider } from "@/lib/context";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { BrainsList } from "./[brainId]/components";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  const { session } = useSupabase();
  if (session === null) {
    redirectToLogin();
  }

  return (
    <div className="relative h-full w-full flex justify-stretch items-stretch">
      <BrainsList />
      <KnowledgeProvider>{children}</KnowledgeProvider>
    </div>
  );
};

export default Layout;
