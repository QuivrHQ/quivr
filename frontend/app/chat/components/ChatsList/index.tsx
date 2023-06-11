"use client";
import useChatsContext from "../../ChatsProvider/hooks/useChatsContext";
import ChatsListItem from "./ChatsListItem";
import { NewChatButton } from "./NewChatButton";
export function ChatsList() {
  const { allChats, deleteChat } = useChatsContext();
  return (
    <div className="sticky top-0 max-h-screen overflow-auto scrollbar">
      <aside className="relative bg-white dark:bg-black max-w-xs w-full border-r border-black/10 dark:border-white/25 h-screen">
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
    </div>
  );
}
