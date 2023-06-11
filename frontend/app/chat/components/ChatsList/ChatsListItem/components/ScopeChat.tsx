import Button from "@/app/components/ui/Button";
import Modal from "@/app/components/ui/Modal";
import useDocuments from "@/app/explore/hooks/useDocuments";
import { FC } from "react";
import { FaMicroscope } from "react-icons/fa";
import fetchFileSHA1 from "../helpers/fetchFileSHA1";

interface ScopeChatProps {}

const ScopeChat: FC<ScopeChatProps> = ({}) => {
  const { isPending, documents } = useDocuments();

  return (
    <Modal
      title="Select the scope of your chat"
      desc="You can select the specific files which you want to chat with here"
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
      {documents.map((document) => (
        <div>
          <Button
            onClick={async () => {
              const sha = await fetchFileSHA1(document.name);
              console.log(sha);
            }}
          >
            GLEK
          </Button>
          <p key={document.name + document.size}>{document.name}</p>
        </div>
      ))}
    </Modal>
  );
};

export default ScopeChat;
