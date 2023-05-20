"use client";
import { FC, ReactNode, useState } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { MdClose } from "react-icons/md";
import { AnimatePresence, motion } from "framer-motion";
import Button from "./Button";

interface ModalProps {
  title: string;
  desc: string;
  children?: ReactNode;
  Trigger: ReactNode;
}

const Modal: FC<ModalProps> = ({ title, desc, children, Trigger }) => {
  const [open, setOpen] = useState(false);
  return (
    <Dialog.Root onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        {Trigger}
        {/* <button className="text-violet11 shadow-blackA7 hover:bg-mauve3 inline-flex h-[35px] items-center justify-center rounded-[4px] bg-white px-[15px] font-medium leading-none shadow-[0_2px_10px] focus:shadow-[0_0_0_2px] focus:shadow-black focus:outline-none">
          Edit profile
        </button> */}
      </Dialog.Trigger>
      <AnimatePresence>
        {open ? (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild forceMount>
              <motion.div
                className="fixed inset-0 flex items-center justify-center overflow-auto cursor-pointer bg-black/50 backdrop-blur-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                // transition={{ duration: 0.4, ease: "easeInOut" }}
              >
                <Dialog.Content asChild forceMount>
                  <motion.div
                    initial={{ opacity: 0, y: "-40%" }}
                    animate={{ opacity: 1, y: "0%" }}
                    exit={{ opacity: 0, y: "40%" }}
                    className="w-[90vw] flex flex-col max-w-lg rounded bg-white p-10 shadow-xl focus:outline-none cursor-auto"
                  >
                    <Dialog.Title className="m-0 text-2xl font-bold">
                      {title}
                    </Dialog.Title>

                    <Dialog.Description className="opacity-50">
                      {desc}
                    </Dialog.Description>

                    {children}

                    <Dialog.Close asChild>
                      <Button variant={"secondary"} className="self-end">
                        Done
                      </Button>
                    </Dialog.Close>

                    <Dialog.Close asChild>
                      <button
                        className="absolute top-0 p-5 right-0 inline-flex appearance-none items-center justify-center rounded-full focus:shadow-sm focus:outline-none"
                        aria-label="Close"
                      >
                        <MdClose />
                      </button>
                    </Dialog.Close>
                  </motion.div>
                </Dialog.Content>
              </motion.div>
            </Dialog.Overlay>
          </Dialog.Portal>
        ) : null}
      </AnimatePresence>
    </Dialog.Root>
  );
};

export default Modal;
