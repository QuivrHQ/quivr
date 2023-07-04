"use client";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import { ReactNode, useState } from "react";
import { MdClose } from "react-icons/md";

import { FC } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Button from "./Button";

interface PopoverProps {
  children?: ReactNode;
  Trigger: ReactNode;
}

const Popover: FC<PopoverProps> = ({ children, Trigger }) => {
  const [open, setOpen] = useState(false);
  return (
    <PopoverPrimitive.Root open={open} onOpenChange={setOpen}>
      <PopoverPrimitive.Trigger asChild>{Trigger}</PopoverPrimitive.Trigger>
      <AnimatePresence>
        {open && (
          <PopoverPrimitive.Portal forceMount>
            <PopoverPrimitive.Content forceMount asChild sideOffset={5}>
              <motion.div
                initial={{ opacity: 0, y: -32 }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                exit={{ opacity: 0, y: -32 }}
                transition={{ duration: 0.2, ease: "easeInOut" }}
                className="relative flex flex-col p-4 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg z-50"
              >
                <div className="flex-1">{children}</div>
                <PopoverPrimitive.Close asChild>
                  <Button
                    variant={"secondary"}
                    className="px-3 py-2 self-end mt-4"
                    aria-label="Close"
                  >
                    Done
                  </Button>
                </PopoverPrimitive.Close>
                <PopoverPrimitive.Arrow className="fill-white stroke-gray-300 stroke-2" />
              </motion.div>
            </PopoverPrimitive.Content>
          </PopoverPrimitive.Portal>
        )}
      </AnimatePresence>
    </PopoverPrimitive.Root>
  );
};

export default Popover;
