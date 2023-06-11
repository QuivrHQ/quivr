import Modal from "@/app/components/ui/Modal";
import { FC } from "react";
import { FaMicroscope } from "react-icons/fa";

interface ScopeChatProps {}

const ScopeChat: FC<ScopeChatProps> = ({}) => {
  return (
    <Modal
      Trigger={
        <button
          className="p-2 text-black overflow-visible dark:text-white hover:text-primary"
          type="button"
          aria-label="Change scope"
        >
          <FaMicroscope />
        </button>
      }
    >
      <h1>Hello world</h1>
    </Modal>
  );
};

export default ScopeChat;
