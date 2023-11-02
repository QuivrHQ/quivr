import { motion, MotionConfig } from "framer-motion";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { LuPanelLeftOpen } from "react-icons/lu";

import { SidebarHeader } from "@/lib/components/Sidebar/components/SidebarHeader";
import { useDevice } from "@/lib/hooks/useDevice";
import { cn } from "@/lib/utils";

import {
  SidebarFooter,
  SidebarFooterButtons,
} from "./components/SidebarFooter/SidebarFooter";

type SidebarProps = {
  children: React.ReactNode;
  showButtons?: SidebarFooterButtons[];
};

export const Sidebar = ({
  children,
  showButtons,
}: SidebarProps): JSX.Element => {
  const { isMobile } = useDevice();
  const pathname = usePathname();
  const [open, setOpen] = useState(!isMobile);

  useEffect(() => {
    setOpen(!isMobile);
  }, [isMobile, pathname]);

  return (
    <MotionConfig transition={{ mass: 1, damping: 10, duration: 0.2 }}>
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
        className="flex flex-col fixed sm:sticky top-0 left-0 h-full overflow-visible z-30 border-r border-black/10 dark:border-white/25 bg-white dark:bg-black"
      >
        {!open && (
          <button
            title="Open Sidebar"
            type="button"
            className="absolute p-3 text-2xl bg-red top-5 -right-20 hover:text-primary dark:hover:text-gray-200 transition-colors"
            data-testid="open-sidebar-button"
            onClick={() => setOpen(true)}
          >
            <LuPanelLeftOpen />
          </button>
        )}
        <motion.div
          initial={{
            width: open ? "18rem" : "0px",
          }}
          animate={{
            width: open ? "18rem" : "0px",
            opacity: open ? 1 : 0.5,
            boxShadow: open
              ? "10px 10px 16px rgba(0, 0, 0, 0)"
              : "10px 10px 16px rgba(0, 0, 0, 0.5)",
          }}
          className={cn("overflow-hidden flex flex-col flex-1 max-w-xs")}
          data-testid="sidebar"
        >
          <SidebarHeader setOpen={setOpen} />
          <div className="overflow-auto flex flex-col flex-1">{children}</div>
          {showButtons && <SidebarFooter showButtons={showButtons} />}
        </motion.div>
      </motion.div>
    </MotionConfig>
  );
};
