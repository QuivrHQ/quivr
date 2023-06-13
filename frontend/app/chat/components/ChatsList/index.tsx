"use client";
import { cn } from "@/lib/utils";
import { MotionConfig, motion } from "framer-motion";
import { useState } from "react";
import { MdChevronRight } from "react-icons/md";
import useChatsContext from "../../ChatsProvider/hooks/useChatsContext";
import ChatsListItem from "./ChatsListItem";
import { NewChatButton } from "./NewChatButton";
export function ChatsList() {
  const { allChats, deleteChat } = useChatsContext();

  const [open, setOpen] = useState(false);

  return (
    <MotionConfig transition={{ mass: 1, damping: 10 }}>
      <div className="lg:sticky fixed top-0 left-0 bottom-0 overflow-visible z-30">
        <motion.div
          animate={{ width: open ? "fit-content" : 0 }}
          className={cn("overflow-hidden", {
            "shadow-lg": open,
          })}
        >
          <div className="min-w-fit max-h-screen border-r border-black/10 dark:border-white/25 bg-white dark:bg-black overflow-auto scrollbar">
            <aside className="relative max-w-xs w-full h-screen">
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
        </motion.div>
        <button
          onClick={() => {
            setOpen(!open);
          }}
          className="absolute left-full top-16 lg:top-0 text-3xl bg-black dark:bg-white text-white dark:text-black rounded-r-full"
        >
          <motion.div
            whileTap={{ scale: 0.9 }}
            animate={{ scaleX: open ? -1 : 1 }}
          >
            <MdChevronRight />
          </motion.div>
        </button>
      </div>
    </MotionConfig>
  );
}
