"use client";

import { MdDelete } from "react-icons/md";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { Knowledge } from "@/lib/types/Knowledge";

import { useKnowledgeItem } from "./useKnowledgeItem";

export const DeleteKnowledge = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  const { isDeleting, onDeleteKnowledge } = useKnowledgeItem();

  const { currentBrain } = useBrainContext();

  const canDeleteFile = currentBrain?.role === "Owner";

  console.log("isDeleting", isDeleting);

  return (
    <>
      {canDeleteFile && (
        <button
          className="text-red-600 hover:text-red-900"
          onClick={() => void onDeleteKnowledge(knowledge)}
        >
          <MdDelete size="20" />
        </button>
      )}
    </>
  );
};
