/* eslint-disable */
"use client";
import useChatsContext from "@/lib/context/ChatsProvider/hooks/useChatsContext";
import { cn } from "@/lib/utils";
import { MotionConfig, motion } from "framer-motion";
import { MdChevronRight } from "react-icons/md";

import { NewChatButton } from "./NewChatButton";
import { ChatsListItem } from "./components/ChatsListItem/";
import { MiniFooter } from "./components/ChatsListItem/components/MiniFooter";
import { useChatsList } from "./hooks/useChatsList";

export const ChatsList = (): JSX.Element => {
  const { allChats, deleteChat } = useChatsContext();
  const { open, setOpen } = useChatsList();
  return (
    <MotionConfig transition={{ mass: 1, damping: 10 }}>
      <motion.div
        drag="x"
        dragConstraints={{ right: 0, left: 0 }}
        // dragSnapToOrigin
        dragElastic={0.15}
        onDragEnd={(event, info) => {
          if (info.offset.x > 100 && !open) {
            setOpen(true);
          } else if (info.offset.x < -100 && open) {
            setOpen(false);
          }
        }}
        className="lg:sticky fixed top-0 left-0 bottom-0 overflow-visible z-30 border-r border-black/10 dark:border-white/25 bg-white dark:bg-black"
      >
        <motion.div
          animate={{
            width: open ? "fit-content" : "0px",
            opacity: open ? 1 : 0.5,
            boxShadow: open
              ? "10px 10px 16px rgba(0, 0, 0, 0)"
              : "10px 10px 16px rgba(0, 0, 0, 0.5)",
            // shadow: open ? "none" : "10px 10px 16px black",
          }}
          className={cn("overflow-hidden")}
        >
          <div className="min-w-fit max-h-screen  overflow-auto scrollbar">
            <aside className="relative max-w-xs w-full h-screen">
              <NewChatButton />
              <div className="flex flex-col gap-0">
                {allChats.map((chat) => (
                  <ChatsListItem
                    key={chat.chat_id}
                    chat={chat}
                    deleteChat={deleteChat}
                  />
                ))}
              </div>
            </aside>
            <div className="fixed bottom-0 left-0 p-4 py-1 absolute w-full bg-white">
              <MiniFooter />
            </div>
          </div>
        </motion.div>
        <button
          onClick={() => {
            setOpen(!open);
          }}
          className="absolute left-full top-16 lg:top-0 text-3xl bg-black dark:bg-white text-white dark:text-black rounded-r-full p-3 pl-1"
        >
          <motion.div
            whileTap={{ scale: 0.9 }}
            animate={{ scaleX: open ? -1 : 1 }}
          >
            <MdChevronRight />
          </motion.div>
        </button>
      </motion.div>
    </MotionConfig>
  );
};
