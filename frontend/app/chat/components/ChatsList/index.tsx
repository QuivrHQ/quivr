"use client";

import { Sidebar } from "@/lib/components/Sidebar/Sidebar";

import { ChatHistory } from "./components/ChatHistory";
import { NewChatButton } from "./components/NewChatButton";
import { SidebarActions } from "./components/SidebarFooter/SidebarActions";
import { SidebarHeader } from "./components/SidebarHeader";
import { useChatNotificationsSync } from "./hooks/useChatNotificationsSync";
import { useChatsList } from "./hooks/useChatsList";

export const ChatsList = (): JSX.Element => {
  useChatsList();
  useChatNotificationsSync();

  return (
    <Sidebar>
      <div className="flex flex-col flex-1 h-full">
        <SidebarHeader />
        <div className="pt-2">
          <NewChatButton />
        </div>
        <ChatHistory />
        <SidebarActions />
      </div>
    </Sidebar>
  );
};
