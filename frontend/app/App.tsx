"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { PropsWithChildren, useEffect } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { UpdateMetadata } from "@/lib/helpers/updateMetadata";
import { redirectToChat } from "@/lib/router/redirectToChat";
import { usePageTracking } from "@/services/analytics/june/usePageTracking";
import { useSecurity } from "@/services/useSecurity/useSecurity";
import "../lib/config/LocaleConfig/i18n";

const queryClient = new QueryClient();

// This wrapper is used to make effect calls at a high level in app rendering.
export const App = ({ children }: PropsWithChildren): JSX.Element => {
  const { isStudioMember, isRouteAccessible } = useSecurity();

  if (!isStudioMember && !isRouteAccessible) {
    redirectToChat();
  }

  const { fetchAllBrains, fetchDefaultBrain, fetchPublicPrompts } =
    useBrainContext();
  const { session } = useSupabase();

  usePageTracking();

  useEffect(() => {
    if (session?.user) {
      void fetchAllBrains();
      void fetchDefaultBrain();
      void fetchPublicPrompts();
    }
  }, [session]);

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <UpdateMetadata />
    </QueryClientProvider>
  );
};
