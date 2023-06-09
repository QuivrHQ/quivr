"use client";
import { UUID } from "crypto";
import Link from "next/link";
import { useEffect } from "react";
import { FiTrash } from "react-icons/fi";
import useChats from "../hooks/useChats";
import { NewChatButton } from "./NewChatButton";
export function ChatsList({ currentChatId }: { currentChatId?: UUID }) {
  const { allChats, deleteChat } = useChats();
  return (
    <div>
      <NewChatButton />
      <h2 className="text-2xl font-bold mb-4">Your chats</h2>
      {allChats.map((chat) => (
        <Link href={`/chat/${chat.chatId}`} key={chat.chatId}>
          <div className="block mb-4 border rounded overflow-hidden shadow-md">
            <div className="px-4 py-2">
              <div className="font-bold text-xl mb-2">
                Chat ID: {chat.chatId}
              </div>
              <p className="text-gray-700 text-base">
                Last message: {"New Chat"}
              </p>
              <button type="button" onClick={() => deleteChat(chat.chatId)}>
                <FiTrash className="hover:text-red-700" />
              </button>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
