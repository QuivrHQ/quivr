"use client";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode, useEffect, useState } from "react";

import styles from "./Tooltip.module.scss";

interface TooltipProps {
  children?: ReactNode;
  tooltip?: ReactNode;
  small?: boolean;
  type?: "default" | "dangerous" | "success";
  delayDuration?: number;
  open?: boolean; // Optional boolean prop
}

const Tooltip = ({
  children,
  tooltip,
  small,
  type,
  delayDuration = 0,
  open: controlledOpen, // Renamed to avoid conflict with state variable
}: TooltipProps): JSX.Element => {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (controlledOpen !== undefined) {
      setOpen(controlledOpen);
    }
  }, [controlledOpen]);

  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root
        onOpenChange={setOpen}
        open={open}
        delayDuration={delayDuration}
      >
        <TooltipPrimitive.Trigger asChild>{children}</TooltipPrimitive.Trigger>
        <AnimatePresence>
          {open && (
            <TooltipPrimitive.Portal forceMount>
              <TooltipPrimitive.Content sideOffset={5} asChild>
                <motion.div
                  initial={{ y: 10, opacity: 0 }}
                  animate={{
                    y: 0,
                    opacity: 1,
                    transition: { ease: "easeOut", duration: 0.1 },
                  }}
                  exit={{
                    y: 10,
                    opacity: 0,
                    transition: { ease: "easeIn", duration: 0.1 },
                  }}
                  className={`${styles.tooltip_content_wrapper} ${
                    small ? styles.small : ""
                  } ${styles[type ?? "default"]}`}
                >
                  {tooltip}
                </motion.div>
              </TooltipPrimitive.Content>
            </TooltipPrimitive.Portal>
          )}
        </AnimatePresence>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
};

export default Tooltip;
