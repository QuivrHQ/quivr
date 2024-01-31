import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { Modal } from "@/lib/components/ui/Modal";
import TextButton from "@/lib/components/ui/TextButton/TextButton";

import { BrainKnowledgeStep } from "./components/BrainKnowledgeStep/BrainKnowledgeStep";
import { BrainParamsStep } from "./components/BrainParamsStep/BrainParamsStep";
import { BrainTypeSelectionStep } from "./components/BrainTypeSelectionStep/BrainTypeSelectionStep";
import { Stepper } from "./components/Stepper/Stepper";
import { useAddBrainConfig } from "./hooks/useAddBrainConfig";

export const AddBrainSteps = ({
  isMenuButton,
}: {
  isMenuButton?: boolean;
}): JSX.Element => {
  const { t } = useTranslation(["translation", "brain", "config"]);

  const { isBrainCreationModalOpened, setIsBrainCreationModalOpened } =
    useAddBrainConfig();

  return (
    <Modal
      Trigger={
        <div onClick={() => void 0}>
          {isMenuButton ? (
            <MenuButton
              iconName="brain"
              label={t("addBrain", { ns: "brain" })}
              type="add"
              color="primary"
            />
          ) : (
            <TextButton
              iconName="add"
              label={t("addBrain", { ns: "brain" })}
              color="black"
            />
          )}
        </div>
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
