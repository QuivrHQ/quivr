import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { Modal } from "@/lib/components/ui/Modal/Modal";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./AddBrainModal.module.scss";
import { useBrainCreationContext } from "./brainCreation-provider";
import { BrainMainInfosStep } from "./components/BrainMainInfosStep/BrainMainInfosStep";

export const AddBrainModal = (): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const { setCurrentBrainId } = useBrainContext();
  const { setSnippetColor, setSnippetEmoji } = useBrainCreationContext();
  const {
    isBrainCreationModalOpened,
    setIsBrainCreationModalOpened,
    setCurrentSelectedBrain,
    setCreating,
  } = useBrainCreationContext();

  useEffect(() => {
    setCurrentSelectedBrain(undefined);
    setCreating(false);
    if (isBrainCreationModalOpened) {
      setCurrentBrainId(null);
      setSnippetColor("#d0c6f2");
      setSnippetEmoji("🧠");
    }
  }, [isBrainCreationModalOpened]);

  return (
    <Modal
      title={t("newBrainTitle", { ns: "brain" })}
      desc={t("newBrainSubtitle", { ns: "brain" })}
      isOpen={isBrainCreationModalOpened}
      setOpen={setIsBrainCreationModalOpened}
      size="big"
      CloseTrigger={<div />}
    >
      <div className={styles.add_brain_modal_container}>
        <div className={styles.content_wrapper}>
          <BrainMainInfosStep />
        </div>
      </div>
    </Modal>
  );
};
