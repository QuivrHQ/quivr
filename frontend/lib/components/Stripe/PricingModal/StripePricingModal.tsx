import { StripePricingTable } from "./components/PricingTable/PricingTable";
import { Modal } from "../../ui/ModalPayment";

type StripePricingModalProps = {
  Trigger: JSX.Element;
};

export const StripePricingModal = ({
  Trigger,
}: StripePricingModalProps): JSX.Element => {
  return (
    <Modal Trigger={Trigger} CloseTrigger={<div />}>
      <StripePricingTable />
    </Modal>
  );
};
