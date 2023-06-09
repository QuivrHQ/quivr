"use client";
import Ellipsis from "@/app/components/ui/Ellipsis";
import Link from "next/link";
import { FiTrash } from "react-icons/fi";
import { MdChat } from "react-icons/md";
import useChats from "../../hooks/useChats";
import { NewChatButton } from "./NewChatButton";
export function ChatsList() {
  const { allChats, deleteChat, chat } = useChats();
  return (
    <aside className="max-w-xs w-full h-full border-r overflow-auto">
      <NewChatButton />
      <h2 className="text-base font-bold p-4">Your chats</h2>
      <div className="flex flex-col gap-0">
        {allChats.map((chat) => (
          <Link href={`/chat/${chat.chatId}`} key={chat.chatId}>
            <div className="block border-b overflow-hidden">
              <div className="p-4">
                <MdChat />
                <Ellipsis
                  maxCharacters={45}
                  className="mb-2 flex-1 text-base leading-none"
                >
                  {chat.history[chat.history.length - 1][1]}
                </Ellipsis>
                <div className="text-xs opacity-50">{chat.chatId}</div>
                <button type="button" onClick={() => deleteChat(chat.chatId)}>
                  <FiTrash className="hover:text-red-700" />
                </button>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </aside>
  );
}
