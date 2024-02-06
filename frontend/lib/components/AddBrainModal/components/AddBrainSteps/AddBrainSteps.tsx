import { useTranslation } from "react-i18next";

import { Modal } from "@/lib/components/ui/Modal";

import { useBrainCreationContext } from "./brainCreation-provider";
import { BrainKnowledgeStep } from "./components/BrainKnowledgeStep/BrainKnowledgeStep";
import { BrainParamsStep } from "./components/BrainParamsStep/BrainParamsStep";
import { BrainTypeSelectionStep } from "./components/BrainTypeSelectionStep/BrainTypeSelectionStep";
import { Stepper } from "./components/Stepper/Stepper";

export const AddBrainSteps = (): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);

  const { isBrainCreationModalOpened, setIsBrainCreationModalOpened } =
    useBrainCreationContext();

  return (
    <Modal
      title={t("newBrainTitle", { ns: "brain" })}
      desc={t("newBrainSubtitle", { ns: "brain" })}
      isOpen={isBrainCreationModalOpened}
      setOpen={setIsBrainCreationModalOpened}
      CloseTrigger={<div />}
    >
      <form
        onSubmit={(e) => {
          e.preventDefault();
        }}
        className="my-10 flex flex-col items-center gap-2 justify-center"
      >
        <Stepper />
        <BrainTypeSelectionStep
          onCancelBrainCreation={() => setIsBrainCreationModalOpened(false)}
        />
        <BrainParamsStep
          onCancelBrainCreation={() => setIsBrainCreationModalOpened(false)}
        />
        <BrainKnowledgeStep
          onCancelBrainCreation={() => setIsBrainCreationModalOpened(false)}
        />
      </form>
    </Modal>
  );
};
