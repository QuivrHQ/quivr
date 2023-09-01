"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { PropsWithChildren, useEffect } from "react";

import Footer from "@/lib/components/Footer";
import { NavBar } from "@/lib/components/NavBar";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { UpdateMetadata } from "@/lib/helpers/updateMetadata";
import { usePageTracking } from "@/services/analytics/usePageTracking";
import "../lib/config/LocaleConfig/i18n";

const queryClient = new QueryClient();

// This wrapper is used to make effect calls at a high level in app rendering.
export const App = ({ children }: PropsWithChildren): JSX.Element => {
  const { fetchAllBrains, fetchAndSetActiveBrain, fetchPublicPrompts } =
    useBrainContext();
  const { session } = useSupabase();

  usePageTracking();

  useEffect(() => {
    void fetchAllBrains();
    void fetchAndSetActiveBrain();
    void fetchPublicPrompts();
  }, [session?.user]);

  return (
    <QueryClientProvider client={queryClient}>
      <NavBar />
      <div className="flex-1">{children}</div>
      <Footer />
      <UpdateMetadata />
    </QueryClientProvider>
  );
};
