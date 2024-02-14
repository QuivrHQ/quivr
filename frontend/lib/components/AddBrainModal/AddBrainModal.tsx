import { FormProvider, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { Modal } from "@/lib/components/ui/Modal/Modal";
import { addBrainDefaultValues } from "@/lib/config/defaultBrainConfig";

import styles from "./AddBrainModal.module.scss";
import { useBrainCreationContext } from "./brainCreation-provider";
import { BrainKnowledgeStep } from "./components/BrainKnowledgeStep/BrainKnowledgeStep";
import { BrainMainInfosStep } from "./components/BrainMainInfosStep/BrainMainInfosStep";
import { BrainTypeSelectionStep } from "./components/BrainTypeSelectionStep/BrainTypeSelectionStep";
import { Stepper } from "./components/Stepper/Stepper";
import { CreateBrainProps } from "./types/types";

export const AddBrainModal = (): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);

  const { isBrainCreationModalOpened, setIsBrainCreationModalOpened } =
    useBrainCreationContext();

  const defaultValues: CreateBrainProps = {
    ...addBrainDefaultValues,
    setDefault: true,
    brainCreationStep: "BRAIN_TYPE",
  };

  const methods = useForm<CreateBrainProps>({
    defaultValues,
  });

  return (
    <FormProvider {...methods}>
      <Modal
        title={t("newBrainTitle", { ns: "brain" })}
        desc={t("newBrainSubtitle", { ns: "brain" })}
        isOpen={isBrainCreationModalOpened}
        setOpen={setIsBrainCreationModalOpened}
        bigModal={true}
        CloseTrigger={<div />}
      >
        <div className={styles.add_brain_modal_container}>
          <div className={styles.stepper_container}>
            <Stepper />
          </div>
          <div className={styles.content_wrapper}>
            <BrainTypeSelectionStep />
            <BrainMainInfosStep />
            <BrainKnowledgeStep />
          </div>
        </div>
      </Modal>
    </FormProvider>
  );
};
