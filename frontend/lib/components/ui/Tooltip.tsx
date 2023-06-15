"use client";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode, useState } from "react";

interface TooltipProps {
  children?: ReactNode;
  tooltip?: ReactNode;
}

const Tooltip = ({ children, tooltip }: TooltipProps): JSX.Element => {
  const [open, setOpen] = useState(false);

  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root onOpenChange={setOpen} open={open}>
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
                  //   transition={{ duration: 0.2, ease: "circInOut" }}
                  className="select-none rounded-md border border-black/10 dark:border-white/25 bg-white dark:bg-gray-800 px-5 py-3 text-sm leading-none shadow-lg dark:shadow-primary/25"
                >
                  {tooltip}
                  <TooltipPrimitive.Arrow className="fill-white dark:fill-black" />
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
