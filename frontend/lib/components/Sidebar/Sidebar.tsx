import { motion, MotionConfig } from "framer-motion";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { LuPanelLeftOpen } from "react-icons/lu";

import { SidebarHeader } from "@/lib/components/Sidebar/components/SidebarHeader";
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
        className="flex flex-col fixed sm:sticky top-0 left-0 h-[100vh] overflow-visible z-30 border-r border-black/10 dark:border-white/25 bg-white dark:bg-black"
      >
        {!open && (
          <button
            title="Open Sidebar"
            type="button"
            className="absolute p-3 text-2xl bg-red top-5 -right-20"
            onClick={() => setOpen(true)}
          >
            <LuPanelLeftOpen />
          </button>
        )}
        <motion.div
          initial={{
            width: open ? "fit-content" : "0px",
          }}
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
          <SidebarHeader setOpen={setOpen} />
          {children}
        </motion.div>
      </motion.div>
    </MotionConfig>
  );
};
