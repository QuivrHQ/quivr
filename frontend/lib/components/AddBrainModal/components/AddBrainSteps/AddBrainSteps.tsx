import { useTranslation } from "react-i18next";
import { LuPlusCircle } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";
import { cn } from "@/lib/utils";

import { BrainKnowledgeStep } from "./components/BrainKnowledgeStep/BrainKnowledgeStep";
import { BrainParamsStep } from "./components/BrainParamsStep/BrainParamsStep";
import { BrainTypeSelectionStep } from "./components/BrainTypeSelectionStep/BrainTypeSelectionStep";
import { Stepper } from "./components/Stepper/Stepper";
import { useAddBrainConfig } from "./hooks/useAddBrainConfig";

type AddBrainConfigProps = {
  triggerClassName?: string;
};

export const AddBrainSteps = ({
  triggerClassName,
}: AddBrainConfigProps): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);

  const { isBrainCreationModalOpened, setIsBrainCreationModalOpened } =
    useAddBrainConfig();

  return (
    <Modal
      Trigger={
        <Button
          onClick={() => void 0}
          variant={"tertiary"}
          className={cn("border-0", triggerClassName)}
          data-testid="add-brain-button"
        >
          <LuPlusCircle className="text-xl" />
          {t("newBrain", { ns: "brain" })}
        </Button>
      }
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
