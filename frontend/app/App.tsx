"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { posthog } from "posthog-js";
import { PostHogProvider } from "posthog-js/react";
import { PropsWithChildren, useEffect } from "react";

import { BrainCreationProvider } from "@/lib/components/AddBrainModal/brainCreation-provider";
import { Menu } from "@/lib/components/Menu/Menu";
import { useOutsideClickListener } from "@/lib/components/Menu/hooks/useOutsideClickListener";
import { SearchModal } from "@/lib/components/SearchModal/SearchModal";
import {
  BrainProvider,
  ChatProvider,
  KnowledgeToFeedProvider,
} from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { ChatsProvider } from "@/lib/context/ChatsProvider";
import { MenuProvider } from "@/lib/context/MenuProvider/Menu-provider";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";
import { NotificationsProvider } from "@/lib/context/NotificationsProvider/notifications-provider";
import { OnboardingProvider } from "@/lib/context/OnboardingProvider/Onboarding-provider";
import { SearchModalProvider } from "@/lib/context/SearchModalProvider/search-modal-provider";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { UserSettingsProvider } from "@/lib/context/UserSettingsProvider/User-settings.provider";
import { IntercomProvider } from "@/lib/helpers/intercom/IntercomProvider";
import { UpdateMetadata } from "@/lib/helpers/updateMetadata";
import { usePageTracking } from "@/services/analytics/june/usePageTracking";

import "../lib/config/LocaleConfig/i18n";
import styles from "./App.module.scss";
import { FromConnectionsProvider } from "./chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/FromConnection-provider";

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
  const { fetchAllBrains } = useBrainContext();
  const { onClickOutside } = useOutsideClickListener();
  const { session } = useSupabase();
  const { isOpened } = useMenuContext();

  usePageTracking();

  useEffect(() => {
    if (session?.user) {
      void fetchAllBrains();

      posthog.identify(session.user.id, { email: session.user.email });
      posthog.startSessionRecording();
    }
  }, [session]);

  return (
    <>
      <PostHogProvider client={posthog}>
        <IntercomProvider>
          <div className="flex flex-1 flex-col overflow-auto">
            <SearchModalProvider>
              <SearchModal />
              <div className={styles.app_container}>
                <div className={styles.menu_container}>
                  <Menu />
                </div>
                <div
                  onClick={onClickOutside}
                  className={`${styles.content_container} ${
                    isOpened ? styles.blured : ""
                  }`}
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
              <NotificationsProvider>
                <MenuProvider>
                  <OnboardingProvider>
                    <FromConnectionsProvider>
                      <ChatsProvider>
                        <ChatProvider>
                          <App>{children}</App>
                        </ChatProvider>
                      </ChatsProvider>
                    </FromConnectionsProvider>
                  </OnboardingProvider>
                </MenuProvider>
              </NotificationsProvider>
            </BrainCreationProvider>
          </KnowledgeToFeedProvider>
        </BrainProvider>
      </UserSettingsProvider>
    </QueryClientProvider>
  );
};

export { AppWithQueryClient as App };
