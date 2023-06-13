import Button from "@/app/components/ui/Button";
import Modal from "@/app/components/ui/Modal";
import { useBrainScope } from "@/lib/context/BrainScopeProvider/hooks/useBrainScope";
import { BrainScope } from "@/lib/context/BrainScopeProvider/types";
import { FC } from "react";
import { FaBrain } from "react-icons/fa";
import DocumentItem from "../../DocumentItem";

interface BrainListItemProps {
  brain: BrainScope;
}

const BrainListItem: FC<BrainListItemProps> = ({ brain }) => {
  const { removeDocumentFromBrain } = useBrainScope();

  return (
    <div className="flex items-center max-w-lg w-full gap-5">
      <div className="flex-1 flex items-center gap-5">
        <FaBrain className="text-4xl" />
        <div className="flex flex-1 flex-col">
          <span className="text-lg font-bold">{brain.name}</span>
          <span className="text-xs">{brain.documents.length} files</span>
        </div>
      </div>
      <Modal
        title={`${brain.name}'s files`}
        desc={brain.id}
        Trigger={<Button>View</Button>}
      >
        <div>
          {brain.documents.map((doc) => (
            <DocumentItem document={doc} setDocuments={() => {}} />
          ))}
        </div>
      </Modal>
    </div>
  );
};

export default BrainListItem;
