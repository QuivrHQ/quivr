/*eslint max-lines: ["error", 200 ]*/

"use client";
import * as Dialog from "@radix-ui/react-dialog";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode, useState } from "react";
import { useTranslation } from "react-i18next";
import { MdClose } from "react-icons/md";

import styles from "./Modal.module.scss";

import Button from "../Button";

type CommonModalProps = {
  title?: string;
  desc?: string;
  children?: ReactNode;
  Trigger?: ReactNode;
  CloseTrigger?: ReactNode;
  isOpen?: undefined;
  setOpen?: undefined;
  bigModal?: boolean;
  unclosable?: boolean;
  unforceWhite?: boolean;
};

type ModalProps =
  | CommonModalProps
  | (Omit<CommonModalProps, "isOpen" | "setOpen"> & {
      isOpen: boolean;
      setOpen: (isOpen: boolean) => void;
    });

const handleInteractOutside = (unclosable: boolean, event: Event) => {
  if (unclosable) {
    event.preventDefault();
  }
};

const handleModalContentAnimation = (
  isOpen: boolean,
  bigModal: boolean,
  unforceWhite: boolean
) => {
  const initialAnimation = { opacity: 0, y: "-40%" };
  const animateAnimation = { opacity: 1, y: "0%" };
  const exitAnimation = { opacity: 0, y: "40%" };

  return {
    initial: initialAnimation,
    animate: animateAnimation,
    exit: exitAnimation,
    className: `${styles.modal_content_wrapper} ${
      bigModal ? styles.big_modal : ""
    } ${unforceWhite ? styles.white : ""}`,
  };
};

export const Modal = ({
  title,
  desc,
  children,
  Trigger,
  CloseTrigger,
  isOpen: customIsOpen,
  setOpen: customSetOpen,
  bigModal,
  unclosable,
  unforceWhite,
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
                className={styles.modal_container}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <Dialog.Content
                  asChild
                  forceMount
                  onInteractOutside={(event) =>
                    handleInteractOutside(!!unclosable, event)
                  }
                >
                  <motion.div
                    {...handleModalContentAnimation(
                      customIsOpen ?? isOpen,
                      !!bigModal,
                      !!unforceWhite
                    )}
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
                    {!unclosable && (
                      <Dialog.Close asChild>
                        <button
                          className={styles.close_button_wrapper}
                          aria-label="Close"
                        >
                          <MdClose />
                        </button>
                      </Dialog.Close>
                    )}
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
