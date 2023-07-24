"use client";
import { ReactNode } from "react";

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
      {children}
    </div>
  );
};

export default Layout;
