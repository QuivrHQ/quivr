import { Modal } from "@/lib/components/ui/Modal/Modal";
import { useUserData } from "@/lib/hooks/useUserData";

import styles from "./AssistantModal.module.scss";

import { Stepper } from "../AddBrainModal/components/Stepper/Stepper";

export const AssistantModal = (): JSX.Element => {
  const { userIdentityData } = useUserData();

  return (
    <Modal
      title="AssistantModal"
      desc={"Description"}
      isOpen={true}
      setOpen={() => console.log("open")}
      unclosable={!userIdentityData?.onboarded}
      size="big"
      CloseTrigger={<div />}
    >
      <div className={styles.add_brain_modal_container}>
        <div className={styles.stepper_container}>
          <Stepper />
        </div>
      </div>
    </Modal>
  );
};
