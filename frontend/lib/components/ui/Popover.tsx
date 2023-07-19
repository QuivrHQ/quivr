"use client";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode, useState } from "react";

import Button from "./Button";

interface PopoverProps {
  children?: ReactNode;
  Trigger: ReactNode;
  ActionTrigger?: ReactNode;
  CloseTrigger?: ReactNode;
}

const Popover = ({
  children,
  Trigger,
  ActionTrigger,
  CloseTrigger,
}: PopoverProps): JSX.Element => {
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
                className="relative flex flex-col p-4 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg z-50 md:z-40"
              >
                <div className="flex-1">{children}</div>
                <div className="mt-4 self-end flex gap-4">
                  {ActionTrigger !== undefined && (
                    <PopoverPrimitive.Close asChild>
                      {ActionTrigger}
                    </PopoverPrimitive.Close>
                  )}
                  <PopoverPrimitive.Close asChild>
                    {CloseTrigger === undefined ? (
                      <Button
                        variant={"secondary"}
                        className="px-3 py-2"
                        aria-label="Close"
                      >
                        Close
                      </Button>
                    ) : (
                      CloseTrigger
                    )}
                  </PopoverPrimitive.Close>
                </div>
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
