import { StripePricingTable } from "./components/PricingTable/PricingTable";

import { Modal } from "../../ui/Modal/Modal";

type StripePricingModalProps = {
  Trigger: JSX.Element;
  user_email: string;
};

export const StripePricingModal = ({
  Trigger,
  user_email,
}: StripePricingModalProps): JSX.Element => {
  return (
    <Modal Trigger={Trigger} CloseTrigger={<div />} unforceWhite={true}>
      <StripePricingTable user_email={user_email} />
    </Modal>
  );
};
