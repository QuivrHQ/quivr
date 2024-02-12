import { useTranslation } from "react-i18next";

import { Modal } from "@/lib/components/ui/Modal/Modal";

import { useBrainCreationContext } from "./brainCreation-provider";

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
      bigModal={true}
      CloseTrigger={<div />}
    ></Modal>
  );
};
