import { useEffect } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { addBrainDefaultValues } from "@/lib/config/defaultBrainConfig";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import styles from "./AddBrainModal.module.scss";
import { useBrainCreationContext } from "./brainCreation-provider";
import { BrainMainInfosStep } from "./components/BrainMainInfosStep/BrainMainInfosStep";
import { BrainRecapStep } from "./components/BrainRecapStep/BrainRecapStep";
import { FeedBrainStep } from "./components/FeedBrainStep/FeedBrainStep";
import { Stepper } from "./components/Stepper/Stepper";
import { useBrainCreationSteps } from "./hooks/useBrainCreationSteps";
import { CreateBrainProps } from "./types/types";

export const AddBrainModal = (): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);
  const { currentStep, steps } = useBrainCreationSteps();
  const { setCurrentBrainId } = useBrainContext();
  const { setSnippetColor, setSnippetEmoji } = useBrainCreationContext();
  const {
    isBrainCreationModalOpened,
    setIsBrainCreationModalOpened,
    setCurrentSelectedBrain,
    setCreating,
  } = useBrainCreationContext();
  const { setCurrentSyncId, setOpenedConnections } =
    useFromConnectionsContext();
  const { removeAllKnowledgeToFeed } = useKnowledgeToFeedContext();

  const defaultValues: CreateBrainProps = {
    ...addBrainDefaultValues,
    setDefault: true,
    brainCreationStep: "FIRST_STEP",
  };

  const methods = useForm<CreateBrainProps>({
    defaultValues,
  });

  useEffect(() => {
    setCurrentSelectedBrain(undefined);
    setCurrentSyncId(undefined);
    setCreating(false);
    setOpenedConnections([]);
    methods.reset(defaultValues);
    removeAllKnowledgeToFeed();
    if (isBrainCreationModalOpened) {
      setCurrentBrainId(null);
      setSnippetColor("#d0c6f2");
      setSnippetEmoji("🧠");
    }
  }, [isBrainCreationModalOpened]);

  return (
    <FormProvider {...methods}>
      <Modal
        title={t("newBrainTitle", { ns: "brain" })}
        desc={t("newBrainSubtitle", { ns: "brain" })}
        isOpen={isBrainCreationModalOpened}
        setOpen={setIsBrainCreationModalOpened}
        size="big"
        CloseTrigger={<div />}
      >
        <div className={styles.add_brain_modal_container}>
          <div className={styles.stepper_container}>
            <Stepper currentStep={currentStep} steps={steps} />
          </div>
          <div className={styles.content_wrapper}>
            <BrainMainInfosStep />
            <FeedBrainStep />
            <BrainRecapStep />
          </div>
        </div>
      </Modal>
    </FormProvider>
  );
};
