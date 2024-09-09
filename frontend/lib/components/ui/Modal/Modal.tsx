/*eslint max-lines: ["error", 200 ]*/

"use client";
import * as Dialog from "@radix-ui/react-dialog";
import { AnimatePresence, motion } from "framer-motion";
import { ReactNode, useState } from "react";
import { useTranslation } from "react-i18next";

import styles from "./Modal.module.scss";

import Button from "../Button";
import { Icon } from "../Icon/Icon";

type CommonModalProps = {
  title?: string;
  desc?: string;
  children?: ReactNode;
  Trigger?: ReactNode;
  CloseTrigger?: ReactNode;
  isOpen?: undefined;
  setOpen?: undefined;
  size?: "auto" | "normal" | "big";
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
  size: "auto" | "normal" | "big",
  unforceWhite: boolean
) => {
  const initialAnimation = { opacity: 0, y: "-40%" };
  const animateAnimation = { opacity: 1, y: "0%" };
  const exitAnimation = { opacity: 0, y: "40%" };

  return {
    initial: initialAnimation,
    animate: animateAnimation,
    exit: exitAnimation,
    className: `${styles.modal_content_wrapper} ${styles[size]} ${
      unforceWhite ? styles.white : ""
    }`,
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
  size = "normal",
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
                    {...handleModalContentAnimation(size, !!unforceWhite)}
                  >
                    <Dialog.Title className={styles.title}>
                      {title}
                    </Dialog.Title>
                    <Dialog.Description className={styles.subtitle}>
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
                          <Icon
                            name="close"
                            color="black"
                            size="normal"
                            handleHover={true}
                          />
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
