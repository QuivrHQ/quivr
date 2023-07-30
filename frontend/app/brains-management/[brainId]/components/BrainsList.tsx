"use client";
import { motion, MotionConfig } from "framer-motion";
import { MdChevronRight } from "react-icons/md";

import { AddBrainModal } from "@/lib/components/AddBrainModal/AddBrainModal";
import { cn } from "@/lib/utils";

import { BrainListItem } from "./BrainListItem";
import { BrainSearchBar } from "./BrainSearchBar";
import { useBrainsList } from "../hooks/useBrainsList";

export const BrainsList = (): JSX.Element => {
  const { open, setOpen, searchQuery, setSearchQuery, brains } =
    useBrainsList();

  return (
    <MotionConfig transition={{ massq: 1, damping: 10 }}>
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
          data-testid="brains-list"
        >
          <div className="flex flex-col flex-1">
            <BrainSearchBar
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
            />
            <div
              data-testid="brains-list-items"
              className="flex-1 overflow-auto scrollbar h-full"
            >
              {brains.map((brain) => (
                <BrainListItem brain={brain} key={brain.id} />
              ))}
            </div>
            <div className="m-2 mb flex flex-col">
              <AddBrainModal />
            </div>
          </div>
        </motion.div>
        <button
          onClick={() => {
            setOpen(!open);
          }}
          className="absolute left-full top-16 text-3xl bg-black dark:bg-white text-white dark:text-black rounded-r-full p-3 pl-1"
          data-testid="brains-list-toggle"
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
