import { UUID } from "crypto";
import { MdContentPaste, MdShare } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import Modal from "@/lib/components/ui/Modal";
import { useToast } from "@/lib/hooks";

type ShareBrainModalProps = {
  brainId: UUID;
};

export const ShareBrain = ({ brainId }: ShareBrainModalProps): JSX.Element => {
  const { publish } = useToast();

  const baseUrl = window.location.origin;
  const brainShareLink = `${baseUrl}/brain_subscription_invitation=${brainId}`;

  const handleCopyInvitationLink = async () => {
    await navigator.clipboard.writeText(brainShareLink);
    publish({
      variant: "success",
      text: "Copied to clipboard",
    });
  };

  return (
    <Modal
      Trigger={
        <Button
          className="group-hover:visible invisible hover:text-red-500 transition-[colors,opacity] p-1"
          onClick={() => void 0}
          variant={"tertiary"}
        >
          <MdShare className="text-xl" />
        </Button>
      }
      title="Share brain"
    >
      <div className="flex flex-row align-center my-5">
        <p>{brainShareLink}</p>
        <Button onClick={() => void handleCopyInvitationLink()}>
          <MdContentPaste />
        </Button>
      </div>
    </Modal>
  );
};
