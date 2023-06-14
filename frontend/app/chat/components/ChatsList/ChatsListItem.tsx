/* eslint-disable */
import { UUID } from "crypto";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { FiTrash2 } from "react-icons/fi";
import { MdChatBubbleOutline } from "react-icons/md";

import { cn } from "@/lib/utils";

import { Chat } from "../../../../lib/types/Chat";

interface ChatsListItemProps {
  chat: Chat;
  deleteChat: (id: UUID) => void;
}

const ChatsListItem = ({
  chat,
  deleteChat,
}: ChatsListItemProps): JSX.Element => {
  const pathname = usePathname()?.split("/").at(-1);
  const selected = chat.chatId === pathname;

  return (
    <div
      className={cn(
        "w-full border-b border-black/10 dark:border-white/25 last:border-none relative group flex overflow-x-hidden hover:bg-gray-100 dark:hover:bg-gray-800",
        selected
          ? "bg-gray-100 dark:bg-gray-800 text-primary dark:text-white"
          : ""
      )}
    >
      <Link
        className="flex flex-col flex-1 min-w-0 p-4"
        href={`/chat/${chat.chatId}`}
        key={chat.chatId}
      >
        <div className="flex items-center gap-2">
          <MdChatBubbleOutline className="text-xl" />

          <p className="min-w-0 flex-1 whitespace-nowrap">{chat.chatName}</p>
        </div>
        <div className="grid-cols-2 text-xs opacity-50 whitespace-nowrap">
          {chat.chatId}
        </div>
      </Link>
      <div className="opacity-0 group-hover:opacity-100 flex items-center justify-center hover:text-red-700 bg-gradient-to-l from-white dark:from-black to-transparent z-10 transition-opacity">
        <button
          className="p-5"
          type="button"
          onClick={() => deleteChat(chat.chatId)}
        >
          <FiTrash2 />
        </button>
      </div>

      {/* Fade to white */}
      <div
        aria-hidden
        className="not-sr-only absolute left-1/2 top-0 bottom-0 right-0 bg-gradient-to-r from-transparent to-white dark:to-black pointer-events-none"
      ></div>
    </div>
  );
};

export default ChatsListItem;
