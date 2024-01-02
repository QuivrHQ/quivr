"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { posthog } from "posthog-js";
import { PostHogProvider } from "posthog-js/react";
import { PropsWithChildren, useEffect } from "react";

import { Menu } from "@/lib/components/Menu/Menu";
import { useOutsideClickListener } from "@/lib/components/Menu/hooks/useOutsideClickListener";
import { NotificationBanner } from "@/lib/components/NotificationBanner";
import { BrainProvider } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { SideBarProvider } from "@/lib/context/SidebarProvider/sidebar-provider";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { UpdateMetadata } from "@/lib/helpers/updateMetadata";
import { usePageTracking } from "@/services/analytics/june/usePageTracking";

import "../lib/config/LocaleConfig/i18n";

if (
  process.env.NEXT_PUBLIC_POSTHOG_KEY != null &&
  process.env.NEXT_PUBLIC_POSTHOG_HOST != null
) {
  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST,
    opt_in_site_apps: true,
    disable_session_recording: true,
  });
}

// This wrapper is used to make effect calls at a high level in app rendering.
const App = ({ children }: PropsWithChildren): JSX.Element => {
  const { fetchAllBrains, fetchDefaultBrain, fetchPublicPrompts } =
    useBrainContext();
  const { onClickOutside } = useOutsideClickListener();
  const { session } = useSupabase();

  usePageTracking();

  useEffect(() => {
    if (session?.user) {
      void fetchAllBrains();
      void fetchDefaultBrain();
      void fetchPublicPrompts();
      posthog.identify(session.user.id, { email: session.user.email });
      posthog.startSessionRecording();
    }
  }, [session]);

  return (
    <PostHogProvider client={posthog}>
      <div className="flex flex-1 flex-col overflow-auto">
        <NotificationBanner />
        <div className="relative h-full w-full flex justify-stretch items-stretch overflow-auto">
          <Menu />
          <div onClick={onClickOutside} className="flex-1">
            {children}
          </div>
          <UpdateMetadata />
        </div>
      </div>
    </PostHogProvider>
  );
};

const queryClient = new QueryClient();

const AppWithQueryClient = ({ children }: PropsWithChildren): JSX.Element => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrainProvider>
        <SideBarProvider>
          <App>{children}</App>
        </SideBarProvider>
      </BrainProvider>
    </QueryClientProvider>
  );
};

export { AppWithQueryClient as App };
