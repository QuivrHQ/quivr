"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Script from "next/script";
import { posthog } from "posthog-js";
import { PostHogProvider } from "posthog-js/react";
import { PropsWithChildren, useEffect } from "react";

import { BrainCreationProvider } from "@/lib/components/AddBrainModal/brainCreation-provider";
import { Menu } from "@/lib/components/Menu/Menu";
import { useOutsideClickListener } from "@/lib/components/Menu/hooks/useOutsideClickListener";
import SearchModal from "@/lib/components/SearchModal/SearchModal";
import {
  BrainProvider,
  ChatProvider,
  KnowledgeToFeedProvider,
} from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { ChatsProvider } from "@/lib/context/ChatsProvider";
import { MenuProvider } from "@/lib/context/MenuProvider/Menu-provider";
import { OnboardingProvider } from "@/lib/context/OnboardingProvider/Onboarding-provider";
import { SearchModalProvider } from "@/lib/context/SearchModalProvider/search-modal-provider";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { UserSettingsProvider } from "@/lib/context/UserSettingsProvider/User-settings.provider";
import { IntercomProvider } from "@/lib/helpers/intercom/IntercomProvider";
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
    <>
      <Script
        id="octolane-script"
        src="https://cdn.octolane.com/tag.js?pk=0a213725640302dff773"
      />

      <PostHogProvider client={posthog}>
        <IntercomProvider>
          <div className="flex flex-1 flex-col overflow-auto">
            <SearchModalProvider>
              <SearchModal />
              <div className="relative h-full w-full flex justify-stretch items-stretch overflow-auto">
                <Menu />
                <div
                  onClick={onClickOutside}
                  className="flex-1 overflow-scroll"
                >
                  {children}
                </div>
                <UpdateMetadata />
              </div>
            </SearchModalProvider>
          </div>
        </IntercomProvider>
      </PostHogProvider>
    </>
  );
};

const queryClient = new QueryClient();

const AppWithQueryClient = ({ children }: PropsWithChildren): JSX.Element => {
  return (
    <QueryClientProvider client={queryClient}>
      <UserSettingsProvider>
        <BrainProvider>
          <KnowledgeToFeedProvider>
            <BrainCreationProvider>
              <MenuProvider>
                <OnboardingProvider>
                  <ChatsProvider>
                    <ChatProvider>
                      <App>{children}</App>
                    </ChatProvider>
                  </ChatsProvider>
                </OnboardingProvider>
              </MenuProvider>
            </BrainCreationProvider>
          </KnowledgeToFeedProvider>
        </BrainProvider>
      </UserSettingsProvider>
    </QueryClientProvider>
  );
};

export { AppWithQueryClient as App };
