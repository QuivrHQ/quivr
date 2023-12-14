"use client";

import { ChatHistory } from "@/lib/components/ChatHistory/ChatHistory";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { WelcomeChat } from "./components/WelcomeChat";
import { useChatNotificationsSync } from "./hooks/useChatNotificationsSync";
import { useChatsList } from "./hooks/useChatsList";

export const ChatsList = (): JSX.Element => {
  useChatsList();
  useChatNotificationsSync();
  const { shouldDisplayWelcomeChat } = useOnboarding();

  return (
    <div className="flex flex-col flex-1 h-full" data-testid="chats-list">
      {shouldDisplayWelcomeChat && (
        <div className="pt-2">
          <WelcomeChat />
        </div>
      )}
      <ChatHistory />
    </div>
  );
};
