"use client";
import { useAxios } from "@/lib/useAxios";
import { UUID } from "crypto";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context";
import Link from "next/link";
import { Dispatch, SetStateAction, useEffect } from "react";
import { FiTrash } from "react-icons/fi";
import { Chat } from "../types";
import { NewChatButton } from "./NewChatButton";
export function ChatsList({
  chats,
  setChats,
  currentChatId,
  router,
}: {
  chats: Chat[];
  setChats: Dispatch<SetStateAction<Chat[]>>;
  currentChatId?: UUID;
  router: AppRouterInstance;
}) {
  const { axiosInstance } = useAxios();
  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await axiosInstance.get<{
          chats: Chat[];
        }>("/chat");
        setChats(response.data.chats);
      } catch (error) {
        console.error("Error fetching chats:", error);
      }
    };

    fetchChats();
  }, [axiosInstance, setChats]);

  const handleDeleteChat = async (chatId: UUID) => {
    try {
      await axiosInstance.delete(`/chat/${chatId}`);
      setChats(chats.filter((chat) => chat.chatId !== chatId));
      //DOES NOT WORK
      // check if the current chat is the one being deleted
      if (currentChatId === chatId) {
        // redirect to the new chat page
        router.push("/chat");
      }
    } catch (error) {
      console.error("Error deleting chat:", error);
    }
  };

  return (
    <div>
      <NewChatButton />
      <h2 className="text-2xl font-bold mb-4">Your chats</h2>
      {chats.map((chat) => (
        <Link href={`/chat/${chat.chatId}`} key={chat.chatId}>
          <div className="block mb-4 border rounded overflow-hidden shadow-md">
            <div className="px-4 py-2">
              <div className="font-bold text-xl mb-2">
                Chat ID: {chat.chatId}
              </div>
              <p className="text-gray-700 text-base">
                Last message: {"New Chat"}
              </p>
              <button
                type="button"
                onClick={() => handleDeleteChat(chat.chatId)}
              >
                <FiTrash className="hover:text-red-700" />
              </button>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
