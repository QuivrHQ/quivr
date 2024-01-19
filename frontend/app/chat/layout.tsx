"use client";
import { ReactNode } from "react";

import { KnowledgeToFeedProvider } from "@/lib/context";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  const { session } = useSupabase();

  if (session === null) {
    redirectToLogin();
  }

  return (
    <KnowledgeToFeedProvider>
      <div className="relative h-full w-full flex justify-stretch items-stretch overflow-auto">
        {children}
      </div>
    </KnowledgeToFeedProvider>
  );
};

export default Layout;
