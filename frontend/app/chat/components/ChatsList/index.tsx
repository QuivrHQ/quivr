/* eslint-disable  */
"use client";
import { motion, MotionConfig } from "framer-motion";
import { MdChevronRight } from "react-icons/md";

import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";
import { cn } from "@/lib/utils";

import { useSelectedChatPage } from "../../[chatId]/hooks/useSelectedChatPage";
import { ChatsListItem } from "./components/ChatsListItem";
import { MiniFooter } from "./components/ChatsListItem/components/MiniFooter";
import { NewChatButton } from "./components/NewChatButton";
import { useChatsList } from "./hooks/useChatsList";

export const ChatsList = (): JSX.Element => {
  const { allChats } = useChatsContext();
  const { open, setOpen } = useChatsList();
  useSelectedChatPage();

  // Utility functions for chat categorization
  const isToday = (date: Date) => {
    const today = new Date();

    return date.toDateString() === today.toDateString();
  };
  
  const isYesterday = (date: Date) => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);

    return date.toDateString() === yesterday.toDateString();
  };

  const isWithinLast7Days = (date: Date) => {
    const today = new Date();
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);

    return date > weekAgo && !isToday(date) && !isYesterday(date);
  };

  const isWithinLast30Days = (date: Date) => {
    const today = new Date();
    const monthAgo = new Date();
    monthAgo.setDate(monthAgo.getDate() - 30);

    return date > monthAgo && !isToday(date) && !isYesterday(date) && !isWithinLast7Days(date);
  };

  // Filtering chats into different groups
  const todayChats = allChats.filter(chat => isToday(new Date(chat.creation_time)));
  const yesterdayChats = allChats.filter(chat => isYesterday(new Date(chat.creation_time)));
  const last7DaysChats = allChats.filter(chat => isWithinLast7Days(new Date(chat.creation_time)));
  const last30DaysChats = allChats.filter(chat => isWithinLast30Days(new Date(chat.creation_time)));

  return (
    <MotionConfig transition={{ mass: 1, damping: 10 }}>
      <motion.div
        drag="x"
        dragConstraints={{ right: 0, left: 0 }}
        dragElastic={0.15}
        onDragEnd={(event, info) => {
          if (info.offset.x > 100 && !open) {
            setOpen(true);
          } else if (info.offset.x < -100 && open) {
            setOpen(false);
          }
        }}
        className="flex flex-col lg:sticky fixed top-16 left-0 bottom-0 lg:h-[90vh] overflow-visible z-30 border-r border-black/10 dark:border-white/25 bg-white dark:bg-black"
      >
        <motion.div
          animate={{
            width: open ? "fit-content" : "0px",
            opacity: open ? 1 : 0.5,
            boxShadow: open
              ? "10px 10px 16px rgba(0, 0, 0, 0)"
              : "10px 10px 16px rgba(0, 0, 0, 0.5)",
          }}
          className={cn("overflow-hidden flex flex-col flex-1")}
          data-testid="chats-list"
        >
          <div className="flex flex-col flex-1 h-full">
            <NewChatButton />
            <div
              data-testid="chats-list-items"
              className="flex-1 overflow-auto scrollbar h-full"
            >
              {todayChats.length > 0 && <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">Today</div>}
              {todayChats.map((chat) => (
                <ChatsListItem key={chat.chat_id} chat={chat} />
              ))}

              {yesterdayChats.length > 0 && <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">Yesterday</div>}
              {yesterdayChats.map((chat) => (
                <ChatsListItem key={chat.chat_id} chat={chat} />
              ))}

              {last7DaysChats.length > 0 && <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">Previous 7 Days</div>}
              {last7DaysChats.map((chat) => (
                <ChatsListItem key={chat.chat_id} chat={chat} />
              ))}

              {last30DaysChats.length > 0 && <div className="bg-gray-100 text-black rounded-md px-3 py-1 mt-2">Previous 30 Days</div>}
              {last30DaysChats.map((chat) => (
                <ChatsListItem key={chat.chat_id} chat={chat} />
              ))}

            </div>
            <MiniFooter />
          </div>
        </motion.div>
        <button
          onClick={() => {
            setOpen(!open);
          }}
          className="absolute left-full top-16 text-3xl bg-black dark:bg-white text-white dark:text-black rounded-r-full p-3 pl-1"
          data-testid="chats-list-toggle"
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
