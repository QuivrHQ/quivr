/*eslint max-lines: ["error", 200 ]*/

"use client";
import * as Dialog from "@radix-ui/react-dialog";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode, useState } from "react";
import { useTranslation } from "react-i18next";
import { MdClose } from "react-icons/md";

import Button from "./Button";

type CommonModalProps = {
  title?: string;
  desc?: string;
  children?: ReactNode;
  Trigger?: ReactNode;
  CloseTrigger?: ReactNode;
  isOpen?: undefined;
  setOpen?: undefined;
};

type ModalProps =
  | CommonModalProps
  | (Omit<CommonModalProps, "isOpen" | "setOpen"> & {
      isOpen: boolean;
      setOpen: (isOpen: boolean) => void;
    });

export const Modal = ({
  title,
  desc,
  children,
  Trigger,
  CloseTrigger,
  isOpen: customIsOpen,
  setOpen: customSetOpen,
}: ModalProps): JSX.Element => {
  const [isOpen, setOpen] = useState(false);
  const { t } = useTranslation(["translation"]);

  return (
    <Dialog.Root
      open={customIsOpen ?? isOpen}
      onOpenChange={customSetOpen ?? setOpen}
    >
      {Trigger !== undefined && (
        <Dialog.Trigger asChild>{Trigger}</Dialog.Trigger>
      )}
      <AnimatePresence>
        {customIsOpen ?? isOpen ? (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild forceMount>
              <motion.div
                className="z-50 md:z-40 py-20 fixed inset-0 flex justify-center overflow-auto cursor-pointer bg-black/50 backdrop-blur-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <Dialog.Content asChild forceMount>
                  <motion.div
                    initial={{ opacity: 0, y: "-40%" }}
                    animate={{ opacity: 1, y: "0%" }}
                    exit={{ opacity: 0, y: "40%" }}
                    className="w-[90vw] my-auto flex flex-col h-fit max-w-2xl rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-10 shadow-xl dark:shadow-primary/50 focus:outline-none cursor-auto"
                  >
                    <Dialog.Title
                      className="m-0 text-2xl font-bold"
                      data-testid="modal-title"
                    >
                      {title}
                    </Dialog.Title>
                    <Dialog.Description
                      className="opacity-50"
                      data-testid="modal-description"
                    >
                      {desc}
                    </Dialog.Description>
                    {children}
                    <Dialog.Close asChild>
                      {CloseTrigger !== undefined ? (
                        CloseTrigger
                      ) : (
                        <Button variant={"secondary"} className="self-end">
                          {t("doneButton")}
                        </Button>
                      )}
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
