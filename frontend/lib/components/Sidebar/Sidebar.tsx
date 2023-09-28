"use client";
import { motion, MotionConfig } from "framer-motion";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { MdChevronRight } from "react-icons/md";

import { useDevice } from "@/lib/hooks/useDevice";
import { cn } from "@/lib/utils";

type SidebarProps = {
  children: React.ReactNode;
};

export const Sidebar = ({ children }: SidebarProps): JSX.Element => {
  const { isMobile } = useDevice();
  const pathname = usePathname();
  const [open, setOpen] = useState(!isMobile);

  useEffect(() => {
    setOpen(!isMobile);
  }, [isMobile, pathname, setOpen]);

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
        className="flex flex-col lg:sticky fixed top-0 left-0 bottom-0 lg:h-[100vh] overflow-visible z-30 border-r border-black/10 dark:border-white/25 bg-white dark:bg-black"
      >
        <motion.div
          initial={{ display: open ? "flex" : "none" }}
          animate={{
            width: open ? "fit-content" : "0px",
            opacity: open ? 1 : 0.5,
            boxShadow: open
              ? "10px 10px 16px rgba(0, 0, 0, 0)"
              : "10px 10px 16px rgba(0, 0, 0, 0.5)",
          }}
          className={cn("overflow-hidden flex flex-col flex-1 max-w-xs")}
          data-testid="sidebar"
        >
          {children}
        </motion.div>
        <button
          onClick={() => {
            setOpen(!open);
          }}
          className="absolute left-full top-16 text-3xl bg-black dark:bg-white text-white dark:text-black rounded-r-full p-3 pl-1"
          data-testid="sidebar-toggle"
          title="Toggle Sidebar"
          type="button"
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
