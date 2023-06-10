"use client";
import useChats from "../../hooks/useChats";
import ChatsListItem from "./ChatsListItem";
import { NewChatButton } from "./NewChatButton";
export function ChatsList() {
  const { allChats, deleteChat } = useChats();
  return (
    <aside className="h-screen bg-white dark:bg-black max-w-xs w-full border-r border-black/10 dark:border-white/25 ">
      <NewChatButton />
      <div className="flex flex-col gap-0">
        {allChats.map((chat) => (
          <ChatsListItem
            key={chat.chatId}
            chat={chat}
            deleteChat={deleteChat}
          />
        ))}
      </div>
    </aside>
  );
}
